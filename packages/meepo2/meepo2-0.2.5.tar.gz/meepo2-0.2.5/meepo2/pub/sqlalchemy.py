# -*- coding: utf-8 -*-

"""
The sqlalchemy pub will hook into SQLAlchemy's event system, shape and publish
events with ``table_action pk`` style.

The events pub flow::

    +------------------+         +-----------------------+
    |                  |         |                       |
    |    meepo2.pub     |         |      before_flush     |
    |                  |    +---->                       |
    |  sqlalchemy_pub  |    |    |  record model states  |
    |                  |    |    |                       |
    +---------+--------+    |    +-----------+-----------+
              |             |                |
        hook  |             |                |
              |             |                |
    +---------v--------+    |    +-----------v-----------+
    |                  |    |    |                       |
    |    sqlalchemy    |    |    |     after_commit      |
    |                  +----+---->                       |
    |  session events  |         |  publish model states |
    |                  |         |                       |
    +------------------+         +-----------+-----------+
                                             |
                                       +-----+
                                       |
               +------------------------------------------------+
               |                       |                        |
    +----------+--------+   +----------v---------+   +----------v---------+
    |                   |   |                    |   |                    |
    | table_write event |   | table_update event |   | table_delete event |
    |                   |   |                    |   |                    |
    +-------------------+   +--------------------+   +--------------------+

"""

from __future__ import absolute_import

import logging

import uuid

from sqlalchemy import event

from ..signals import signal


class sqlalchemy_pub(object):
    """SQLAlchemy Pub.

    The install method will add 2 hooks on sqlalchemy events system:

    * ``session_update`` -> sqlalchemy - ``before_flush``
    * ``session_commit`` -> sqlalchemy - ``after_commit``

    The ``session_update`` method need to record the model states in
    sqlalchemy "before_flush" event, when the session records the status
    with ``session.new``, ``session.dirty`` and ``session.deleted``, these
    states will be deleted in "after_commit" event.

    **General Usage**

    Install the sqlalchemy pub hook by calling it on sqlalchemy session::

        sqlalchemy_pub(session)

    Only listen some tables::

        sqlalchemy_pub(session, tables=["test"])

    Tables can be added later, the duplicated tables will be automatically
    merged::

        pub = sqlalchemy_pub(session)
        pub(["table_a", "table_b"])
        pub(["table_b", "table_c"])
        pub.tables == {"table_a", "table_b", "table_c"}

    Then use the session as usual and the events will be available.

    **Signals Illustrate**

    Sometimes you want more info than the pk value, the sqlalchemy_pub expose
    a raw signal which will send the original sqlalchemy objects.

    For example, this code::

        class Test(Base):
            __tablename__ = "test"
            id = Column(Integer, primary_key=True)
            data = Column(String)

        t_1 = Test(id=1, data='a')
        session.add(t_1)
        session.commit()

    Generates signals equal to::

        signal("test_write").send(1)
        signal("test_write_raw").send(t_1)

    :param session: sqlalchemy session to install the hook
    :param tables: tables to install the hook, leave None to pub all.

    .. warning::

        SQLAlchemy bulk operation currently **NOT** supported, so this code
        won't work::

            # bulk updates
            session.query(Test).update({"data": 'x'})

            # bulk deletes
            session.query(Test).filter(Test.data == 'x').delete()
    """

    logger = logging.getLogger("meepo2.pub.sqlalchemy_pub")

    def __init__(self, session, tables=None):
        self.session = session
        self.tables = tables or set()

        self._install()

    def __call__(self, tables):
        self.tables |= set(tables)

    def _install(self):
        # enable session_update & session_commit hook
        event.listen(self.session, "before_flush", self.session_update)
        event.listen(self.session, "after_commit", self.session_commit)

    def _pk(self, obj):
        """Get pk values from object

        :param obj: sqlalchemy object
        """
        pk_values = tuple(getattr(obj, c.name)
                          for c in obj.__mapper__.primary_key)
        if len(pk_values) == 1:
            return pk_values[0]
        return pk_values

    def _session_init(self, session):
        if hasattr(session, "meepo2_unique_id"):
            self.logger.debug("skipped - session_init")
            return

        for action in ("write", "update", "delete"):
            attr = "pending_%s" % action
            if not hasattr(session, attr):
                setattr(session, attr, set())
        session.meepo2_unique_id = uuid.uuid4().hex
        self.logger.debug("%s - session_init" % session.meepo2_unique_id)

    def _session_del(self, session):
        self.logger.debug("%s - session_del" % session.meepo2_unique_id)
        del session.meepo2_unique_id
        del session.pending_write
        del session.pending_update
        del session.pending_delete

    def _session_pub(self, session):
        def _pub(obj, action):
            """Publish object pk values with action.

            The _pub will trigger 2 signals:
            * normal ``table_action`` signal, sends primary key
            * raw ``table_action_raw`` signal, sends sqlalchemy object

            :param obj: sqlalchemy object
            :param action: action on object
            """
            if self.tables and obj.__table__.fullname not in self.tables:
                return

            sg_name = "%s_%s" % (obj.__table__, action)
            sg = signal(sg_name)
            sg_raw = signal("%s_raw" % sg_name)

            pk = self._pk(obj)
            if pk:
                sg.send(pk)
                sg_raw.send(obj)
                self.logger.debug("%s - session_pub: %s -> %s" % (
                    session.meepo2_unique_id, sg_name, pk))

        for obj in session.pending_write:
            _pub(obj, action="write")
        for obj in session.pending_update:
            _pub(obj, action="update")
        for obj in session.pending_delete:
            _pub(obj, action="delete")

        session.pending_write.clear()
        session.pending_update.clear()
        session.pending_delete.clear()

    def session_update(self, session, *_):
        """Record the sqlalchemy object states in the middle of session,
        prepare the events for the final pub in session_commit.
        """
        self._session_init(session)
        session.pending_write |= set(session.new)
        session.pending_update |= set(session.dirty)
        session.pending_delete |= set(session.deleted)
        self.logger.debug("%s - session_update" % session.meepo2_unique_id)

    def session_commit(self, session):
        """Pub the events after the session committed.

        This method should be linked to sqlalchemy "after_commit" event.
        """
        # this may happen when there's nothing to commit
        if not hasattr(session, 'meepo2_unique_id'):
            self.logger.debug("skipped - session_commit")
            return

        self._session_pub(session)
        self._session_del(session)
