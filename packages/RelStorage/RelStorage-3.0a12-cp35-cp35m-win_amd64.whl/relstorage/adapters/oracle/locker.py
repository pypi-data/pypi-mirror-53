##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
Locker implementations.
"""

from __future__ import absolute_import

from zope.interface import implementer

from ..._compat import metricmethod
from ..interfaces import ILocker
from ..interfaces import UnableToAcquireCommitLockError
from ..interfaces import UnableToAcquirePackUndoLockError
from ..locker import AbstractLocker

from .batch import OracleRowBatcher

@implementer(ILocker)
class OracleLocker(AbstractLocker):

    def __init__(self, options, driver, inputsize_NUMBER):
        super(OracleLocker, self).__init__(
            options=options,
            driver=driver,
            batcher_factory=OracleRowBatcher
        )
        self.inputsize_NUMBER = inputsize_NUMBER

    @metricmethod
    def hold_commit_lock(self, cursor, ensure_current=False, nowait=False):
        # Hold commit_lock to prevent concurrent commits
        # (for as short a time as possible).
        timeout = self.commit_lock_timeout if not nowait else 0
        status = cursor.callfunc(
            "DBMS_LOCK.REQUEST",
            self.inputsize_NUMBER, (
                self.commit_lock_id,
                6,  # exclusive (X_MODE)
                timeout,
                True, # release on commit, yes please
            ))
        if status != 0:
            if nowait and status == 1:
                return False # Lock failed due to a timeout
            if status >= 1 and status <= 5:
                msg = ('', 'timeout', 'deadlock', 'parameter error',
                       'lock already owned', 'illegal handle')[int(status)]
            else:
                msg = str(status)
            raise UnableToAcquireCommitLockError(
                "Unable to acquire commit lock (%s)" % msg)

        # Alternative:
        #cursor.execute("LOCK TABLE commit_lock IN EXCLUSIVE MODE")
        # However, this is known to produce slower results. See
        # https://groups.google.com/d/msg/zodb/IzQoClP5Hgc/8o28J4PkDQAJ

        if ensure_current:
            if self.keep_history:
                # Lock transaction and current_object in share mode to ensure
                # conflict detection has the most current data.
                cursor.execute("LOCK TABLE transaction IN SHARE MODE")
                cursor.execute("LOCK TABLE current_object IN SHARE MODE")
            else:
                cursor.execute("LOCK TABLE object_state IN SHARE MODE")
        return True

    def release_commit_lock(self, cursor):
        # no action needed
        pass

    def hold_pack_lock(self, cursor):
        """Try to acquire the pack lock.

        Raise an exception if packing or undo is already in progress.
        """
        stmt = """
        LOCK TABLE pack_lock IN EXCLUSIVE MODE NOWAIT
        """
        try:
            cursor.execute(stmt)
        except self.lock_exceptions:  # cx_Oracle.DatabaseError:
            raise UnableToAcquirePackUndoLockError('A pack or undo operation is in progress')

    def release_pack_lock(self, cursor):
        """Release the pack lock."""
        # No action needed
