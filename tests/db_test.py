"""Tests for db module"""
import os
import sqlite3
import unittest

import util.db
import util.logger


DB_NAME = 'test.db'
LOGGER = util.logger.logging.getLogger('pkt.util.test')
util.logger.setup()


class TestDB(unittest.TestCase):
    """Tests for db"""

    @staticmethod
    def cleanup():
        """Remove db files."""
        try:
            os.unlink(DB_NAME)
        except FileNotFoundError:
            pass
        assert not os.path.isfile(DB_NAME)

    def setUp(self):
        """Prepare the test fixture"""
        LOGGER.info('setting up')
        self.cleanup()

    def tearDown(self):
        LOGGER.info('tearing down')
        self.cleanup()

    def test_sql(self):
        """Test selecting from just created and filled table"""
        LOGGER.info('creating and filling new table')
        with util.db.sql_connection(DB_NAME) as sql:
            sql.execute('CREATE TABLE test(id INTEGER UNIQUE, number INTEGER)')
            sql.execute('INSERT INTO test (id, number) VALUES (0, 144)')
            sql.execute('INSERT INTO test (id, number) VALUES (1, 13)')
            sql.execute('INSERT INTO test (id, number) VALUES (2, 37)')
        LOGGER.info('selecting data from table')
        with util.db.sql_connection(DB_NAME) as sql:
            sql.execute('SELECT number FROM test WHERE number > 100')
            result = sql.fetchone()
            self.assertNotEqual(result, None)
            self.assertEqual(result[0], 144)

    def test_closing(self):
        """Test closing connection"""
        LOGGER.info('creating new table')
        with util.db.sql_connection(DB_NAME) as sql:
            sql.execute('CREATE TABLE test(id INTEGER UNIQUE, number INTEGER)')
        LOGGER.info('attempting operation after closing connection')
        self.assertRaises(sqlite3.ProgrammingError, sql.fetchone)

    def test_closing_on_exception(self):
        """Test closing connection on exception"""
        LOGGER.info('expecting raising exception')
        try:
            with util.db.sql_connection(DB_NAME) as sql:
                sql.execute('CREATE TABLE test(id INTEGER UNIQUE, number INTEGER)')
                sql.execute('CREATE TABLE test(id INTEGER UNIQUE, number INTEGER)')  # should raise ProgrammingError
        except:
            pass  # ignore raised Exception
        finally:
            LOGGER.info('attempting operation after raising exception')
            self.assertRaises(sqlite3.ProgrammingError, sql.fetchone)
