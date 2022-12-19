"""
Test custom Django management commands
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# Mocks the method within our command that allows us to check /
# that status of the DB
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTest(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database is ready"""
        # When we call the patched version of the check command listed above, /
        # we just want to return a value
        patched_check.return_value = True

        # Tests that the database is ready, and that the DB is setup  /
        # correctly and can be called
        call_command('wait_for_db')

        # Test that the mocked check command was called, and with the /
        # correct database params
        patched_check.assert_called_once_with(databases=['default'])

    # Params in these functions are listed in order from the inside out
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError"""
        # The first 2 times we call the mocked method, we want to raise a /
        # Psycopg2Error to simulate postgres app not being started
        # The next 3 times we want to raise an OperationalError to simulate /
        # the DB accepting connections but testing DB isn't setup yet
        # The last time it will return True
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
