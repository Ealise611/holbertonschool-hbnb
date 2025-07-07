"""
Basic MySQL pytest test
"""

import pytest

class TestMySQLBasic:
    '''Tests MySQL connection and basic functions'''
    def test_mysql_connection(self, app):
        '''Tests whether we connect to mysql'''
        with app.app_context():
            from app import db
            with db.engine.connect() as conn:
                result = conn.execute(db.text('SELECT DATABASE()'))
                db_name = result.fetchone()[0]
                assert db_name == 'hbnb_pytest_test'
                print(f"✅ Connected to: {db_name}")

    def test_simple_math(self):
        """Basic test to verify pytest is working"""
        assert 2 + 2 == 4
        print("✅ Basic math works!")