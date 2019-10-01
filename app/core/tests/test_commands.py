import sys
from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase
from zeep import Client
from zeep.transports import Transport
from requests import Session

DSVIEW_URL = r'https://nosxihdsview01/dsview/services/UserServiceApi?wsdl'


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db IS available"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)

    def test_zeep_import(self):
        """Test that the zeep module is loaded properly"""
        self.assertTrue('zeep' in sys.modules)

    def test_dsview_wsdl_connection(self):
        """test that the connection to the DSView API is accessible"""
        session = Session()
        session.verify = False
        # session.verify = '/nosxihdsview01.pem'
        transport = Transport(session=session)
        client = Client(DSVIEW_URL, transport=transport)
        client.transport.session.verify = False

        print(client)
