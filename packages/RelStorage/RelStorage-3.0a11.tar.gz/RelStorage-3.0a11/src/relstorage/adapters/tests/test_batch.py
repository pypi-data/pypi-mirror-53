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

from relstorage.tests import TestCase
from relstorage.tests import MockCursor


class RowBatcherTests(TestCase):

    def getClass(self):
        from relstorage.adapters.batch import RowBatcher
        return RowBatcher

    def test_delete_defer(self):
        cursor = MockCursor()
        batcher = self.getClass()(cursor)
        batcher.delete_from("mytable", id=2)
        self.assertEqual(cursor.executed, [])
        self.assertEqual(batcher.rows_added, 1)
        self.assertEqual(batcher.size_added, 0)
        self.assertEqual(batcher.total_rows_inserted, 0)
        self.assertEqual(batcher.total_rows_deleted, 0)
        self.assertEqual(batcher.total_size_inserted, 0)
        self.assertEqual(dict(batcher.deletes),
                         {('mytable', ('id',)): set([(2,)])})

    def test_delete_multiple_column(self):
        cursor = MockCursor()
        batcher = self.getClass()(cursor)
        batcher.delete_from("mytable", id=2, tid=10)
        self.assertEqual(cursor.executed, [])
        self.assertEqual(batcher.rows_added, 1)
        self.assertEqual(batcher.size_added, 0)
        self.assertEqual(dict(batcher.deletes),
                         {('mytable', ('id', 'tid')): set([(2, 10)])})

    def test_delete_auto_flush(self):
        cursor = MockCursor()
        batcher = self.getClass()(cursor, 2)
        batcher.sorted_deletes = True
        batcher.delete_from("mytable", id=2)
        batcher.delete_from("mytable", id=1)
        self.assertEqual(cursor.executed,
                         [('DELETE FROM mytable WHERE id IN (%s,%s)', ((1, 2)))])
        self.assertEqual(batcher.rows_added, 0)
        self.assertEqual(batcher.size_added, 0)
        self.assertEqual(batcher.deletes, {})
        self.assertEqual(batcher.total_rows_inserted, 0)
        self.assertEqual(batcher.total_rows_deleted, 2)
        self.assertEqual(batcher.total_size_inserted, 0)

    def test_insert_defer(self):
        cursor = MockCursor()
        batcher = self.getClass()(cursor)
        batcher.insert_into(
            "mytable (id, name)",
            "%s, id || %s",
            (1, 'a'),
            rowkey=1,
            size=3,
        )
        self.assertEqual(cursor.executed, [])
        self.assertEqual(batcher.rows_added, 1)
        self.assertEqual(batcher.size_added, 3)
        self.assertEqual(batcher.inserts, {
            ('INSERT', 'mytable (id, name)', '%s, id || %s', ''): {1: (1, 'a')}
        })
        self.assertEqual(batcher.total_rows_inserted, 0)
        self.assertEqual(batcher.total_rows_deleted, 0)
        self.assertEqual(batcher.total_size_inserted, 0)

    def test_insert_defer_multi_table(self):
        cursor = MockCursor()
        batcher = self.getClass()(cursor)
        batcher.insert_into(
            "mytable (id, name)",
            "%s, id || %s",
            (1, 'a'),
            rowkey=1,
            size=3,
        )
        batcher.insert_into(
            "othertable (name)",
            "?",
            ('a'),
            rowkey=1,
            size=1,
        )

        self.assertEqual(cursor.executed, [])
        self.assertEqual(batcher.rows_added, 2)
        self.assertEqual(batcher.size_added, 4)
        self.assertEqual(dict(batcher.inserts), {
            ('INSERT', 'mytable (id, name)', '%s, id || %s', ''): {1: (1, 'a')},
            ('INSERT', 'othertable (name)', '?', ''): {1: ('a')},
        })
        self.assertEqual(batcher.total_rows_inserted, 0)
        self.assertEqual(batcher.total_rows_deleted, 0)
        self.assertEqual(batcher.total_size_inserted, 0)

    def test_insert_replace(self):
        cursor = MockCursor()
        batcher = self.getClass()(cursor)
        batcher.insert_into(
            "mytable (id, name)",
            "%s, id || %s",
            (1, 'a'),
            rowkey=1,
            size=3,
            command='REPLACE',
        )
        self.assertEqual(cursor.executed, [])
        self.assertEqual(batcher.rows_added, 1)
        self.assertEqual(batcher.size_added, 3)
        self.assertEqual(batcher.inserts, {
            ('REPLACE', 'mytable (id, name)', '%s, id || %s', ''): {1: (1, 'a')}
        })

    def test_insert_duplicate(self):
        # A second insert on the same rowkey replaces the first insert.
        cursor = MockCursor()
        batcher = self.getClass()(cursor)
        batcher.insert_into(
            "mytable (id, name)",
            "%s, id || %s",
            (1, 'a'),
            rowkey=1,
            size=3,
            )
        batcher.insert_into(
            "mytable (id, name)",
            "%s, id || %s",
            (1, 'b'),
            rowkey=1,
            size=3,
            )
        self.assertEqual(cursor.executed, [])
        self.assertEqual(batcher.rows_added, 2)
        self.assertEqual(batcher.size_added, 6)
        self.assertEqual(batcher.inserts, {
            ('INSERT', 'mytable (id, name)', '%s, id || %s', ''): {1: (1, 'b')}
        })

    def test_insert_auto_flush(self):
        cursor = MockCursor()
        batcher = self.getClass()(cursor)
        batcher.size_limit = 10
        batcher.insert_into(
            "mytable (id, name)",
            "%s, id || %s",
            (1, 'a'),
            rowkey=1,
            size=5,
            )
        batcher.insert_into(
            "mytable (id, name)",
            "%s, id || %s",
            (2, 'B'),
            rowkey=2,
            size=5,
            )
        self.assertEqual(
            cursor.executed,
            [(
                'INSERT INTO mytable (id, name) VALUES\n'
                '(%s, id || %s),\n'
                '(%s, id || %s)\n',
                (1, 'a', 2, 'B'))
            ])
        self.assertEqual(batcher.rows_added, 0)
        self.assertEqual(batcher.size_added, 0)
        self.assertEqual(batcher.inserts, {})
        self.assertEqual(batcher.total_rows_inserted, 2)
        self.assertEqual(batcher.total_rows_deleted, 0)
        self.assertEqual(batcher.total_size_inserted, 10)


    def test_insert_auto_flush_multi_table(self):
        cursor = MockCursor()
        batcher = self.getClass()(cursor)
        batcher.size_limit = 10
        batcher.insert_into(
            "mytable (id, name)",
            "%s, id || %s",
            (1, 'a'),
            rowkey=1,
            size=5,
            )
        batcher.insert_into(
            "mytable (id, name)",
            "%s, id || %s",
            (2, 'B'),
            rowkey=2,
            size=5,
            )
        self.assertEqual(
            cursor.executed,
            [(
                'INSERT INTO mytable (id, name) VALUES\n'
                '(%s, id || %s),\n'
                '(%s, id || %s)\n',
                (1, 'a', 2, 'B'))
            ])
        self.assertEqual(batcher.rows_added, 0)
        self.assertEqual(batcher.size_added, 0)
        self.assertEqual(batcher.inserts, {})
        self.assertEqual(batcher.total_rows_inserted, 2)
        self.assertEqual(batcher.total_rows_deleted, 0)
        self.assertEqual(batcher.total_size_inserted, 10)

    def test_flush(self):
        cursor = MockCursor()
        batcher = self.getClass()(cursor, delete_placeholder="?")
        # Make sure we preserve order in multi-column
        batcher.sorted_deletes = True
        batcher.delete_from("mytable", id=1)
        batcher.insert_into(
            "mytable (id, name)",
            "%s, id || %s",
            (1, 'a'),
            rowkey=1,
            size=5,
            )
        batcher.delete_from("mytable", id=1, key='abc')
        batcher.delete_from("mytable", id=2, key='def')
        batcher.flush()
        self.assertEqual(cursor.executed, [
            ('DELETE FROM mytable WHERE id IN (?)',
             ((1,))),
            ('DELETE FROM mytable WHERE (id=? AND key=?) OR (id=? AND key=?)',
             (1, 'abc', 2, 'def')),
            ('INSERT INTO mytable (id, name) VALUES\n(%s, id || %s)\n',
             (1, 'a')),
        ])

    def test_select_one(self):
        cursor = MockCursor()
        batcher = self.getClass()(cursor)
        list(batcher.select_from(('zoid', 'tid'), 'object_state', oids=(1,)))
        self.assertEqual(cursor.executed, [
            ('SELECT zoid,tid FROM object_state WHERE oids IN (%s)',
             (1,))
        ])

    def test_select_multiple_one_batch(self):
        cursor = MockCursor()
        batcher = self.getClass()(cursor)
        list(batcher.select_from(('zoid', 'tid'), 'object_state',
                                 oids=(1, 2, 3, 4)))
        self.assertEqual(cursor.executed, [
            ('SELECT zoid,tid FROM object_state WHERE oids IN (%s,%s,%s,%s)',
             (1, 2, 3, 4))
        ])

    def test_select_multiple_many_batch(self):
        cursor = MockCursor()
        cursor.many_results = [
            [(1, 1)],
            [(3, 1)],
            []
        ]
        batcher = self.getClass()(cursor)
        batcher.row_limit = 2
        rows = batcher.select_from(('zoid', 'tid'), 'object_state',
                                   oids=(1, 2, 3, 4, 5))
        rows = list(rows)
        self.assertEqual(cursor.executed, [
            ('SELECT zoid,tid FROM object_state WHERE oids IN (%s,%s)',
             (1, 2,)),
            ('SELECT zoid,tid FROM object_state WHERE oids IN (%s,%s)',
             (3, 4,)),
            ('SELECT zoid,tid FROM object_state WHERE oids IN (%s)',
             (5,)),
        ])

        self.assertEqual(rows, [
            (1, 1),
            (3, 1)
        ])


class OracleRowBatcherTests(TestCase):

    def getClass(self):
        from relstorage.adapters.oracle.batch import OracleRowBatcher
        return OracleRowBatcher

    def test_insert_one_row(self):
        cursor = MockCursor()
        batcher = self.getClass()(cursor, {})
        batcher.insert_into(
            "mytable (id, name)",
            "%s, id || %s",
            (1, 'a'),
            rowkey=1,
            size=3,
            )
        self.assertEqual(cursor.executed, [])
        batcher.flush()
        self.assertEqual(cursor.executed, [
            ('INSERT INTO mytable (id, name) VALUES (%s, id || %s)', (1, 'a')),
            ])

    def test_insert_two_rows(self):
        cursor = MockCursor()
        batcher = self.getClass()(cursor, {})
        batcher.insert_into(
            "mytable (id, name)",
            ":id, :id || :name",
            {'id': 1, 'name': 'a'},
            rowkey=1,
            size=3,
            )
        batcher.insert_into(
            "mytable (id, name)",
            ":id, :id || :name",
            {'id': 2, 'name': 'b'},
            rowkey=2,
            size=3,
            )
        self.assertEqual(cursor.executed, [])
        batcher.flush()
        self.assertEqual(
            cursor.executed,
            [(
                'INSERT ALL\n'
                'INTO mytable (id, name) VALUES (:id_0, :id_0 || :name_0)\n'
                'INTO mytable (id, name) VALUES (:id_1, :id_1 || :name_1)\n'
                'SELECT * FROM DUAL',
                {'id_0': 1, 'id_1': 2, 'name_1': 'b', 'name_0': 'a'})
            ])

    def test_insert_one_raw_row(self):
        class MockRawType(object):
            pass
        cursor = MockCursor()
        batcher = self.getClass()(cursor, {'rawdata': MockRawType})
        batcher.insert_into(
            "mytable (id, data)",
            ":id, :rawdata",
            {'id': 1, 'rawdata': 'xyz'},
            rowkey=1,
            size=3,
            )
        batcher.flush()
        self.assertEqual(cursor.executed, [
            ('INSERT INTO mytable (id, data) VALUES (:id, :rawdata)',
             {'id': 1, 'rawdata': 'xyz'})
        ])
        self.assertEqual(cursor.inputsizes, {'rawdata': MockRawType})

    def test_insert_two_raw_rows(self):
        class MockRawType(object):
            pass
        cursor = MockCursor()
        batcher = self.getClass()(cursor, {'rawdata': MockRawType})
        batcher.insert_into(
            "mytable (id, data)",
            ":id, :rawdata",
            {'id': 1, 'rawdata': 'xyz'},
            rowkey=1,
            size=3,
            )
        batcher.insert_into(
            "mytable (id, data)",
            ":id, :rawdata",
            {'id': 2, 'rawdata': 'abc'},
            rowkey=2,
            size=3,
            )
        batcher.flush()
        self.assertEqual(
            cursor.executed,
            [(
                'INSERT ALL\n'
                'INTO mytable (id, data) VALUES (:id_0, :rawdata_0)\n'
                'INTO mytable (id, data) VALUES (:id_1, :rawdata_1)\n'
                'SELECT * FROM DUAL',
                {'id_0': 1, 'id_1': 2, 'rawdata_0': 'xyz', 'rawdata_1': 'abc'})
            ])
        self.assertEqual(cursor.inputsizes, {
            'rawdata_0': MockRawType,
            'rawdata_1': MockRawType,
        })

class PostgreSQLRowBatcherTests(TestCase):

    def getClass(self):
        from relstorage.adapters.postgresql.batch import PostgreSQLRowBatcher
        return PostgreSQLRowBatcher

    def test_select_one(self):
        cursor = MockCursor()
        batcher = self.getClass()(cursor)
        list(batcher.select_from(('zoid', 'tid'), 'object_state', oids=(1,)))
        self.assertEqual(cursor.executed, [
            ('SELECT zoid,tid FROM object_state WHERE oids = ANY (%s)',
             ([1,],))
        ])

    def test_select_multiple_one_batch(self):
        cursor = MockCursor()
        batcher = self.getClass()(cursor)
        list(batcher.select_from(('zoid', 'tid'), 'object_state',
                                 oids=(1, 2, 3, 4)))
        self.assertEqual(cursor.executed, [
            ('SELECT zoid,tid FROM object_state WHERE oids = ANY (%s)',
             ([1, 2, 3, 4],))
        ])

    def test_select_multiple_many_batch(self):
        cursor = MockCursor()
        cursor.many_results = [
            [(1, 1)],
            [(3, 1)],
            []
        ]
        batcher = self.getClass()(cursor)
        batcher.row_limit = 2
        rows = batcher.select_from(('zoid', 'tid'), 'object_state',
                                   oids=(1, 2, 3, 4, 5))
        rows = list(rows)
        self.assertEqual(cursor.executed, [
            ('SELECT zoid,tid FROM object_state WHERE oids = ANY (%s)',
             ([1, 2,],)),
            ('SELECT zoid,tid FROM object_state WHERE oids = ANY (%s)',
             ([3, 4,],)),
            ('SELECT zoid,tid FROM object_state WHERE oids = ANY (%s)',
             ([5,],)),
        ])

        self.assertEqual(rows, [
            (1, 1),
            (3, 1)
        ])
