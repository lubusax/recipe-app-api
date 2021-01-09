from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """ Are we waiting for db when db is available? """
        # simulate Behavior when the dabase is available
        with patch(
                'django.db.utils.ConnectionHandler.__getitem__') as getitem:
            getitem.return_value = True
            call_command('wait_for_db')
            self.assertEqual(getitem.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, timesleep_patch):
        """ Are we really waiting for db to be available?"""
        with patch(
                'django.db.utils.ConnectionHandler.__getitem__') as getitem:
            # side effect: the first 5 times you call getitem it is going to
            # rise an operational error
            getitem.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(getitem.call_count, 6)
