import errno
import os
import unittest
from unittest.mock import patch, MagicMock


# pylint: disable=wrong-import-position
from aws_gate.session import Session, session # noqa


class TestSession(unittest.TestCase):

    def setUp(self):
        mock_attrs = {
            'get_host.return_value': {}
        }

        self.config = MagicMock()
        self.empty_config = MagicMock()
        self.empty_config.configure_mock(**mock_attrs)
        self.ssm = MagicMock()
        self.instance_id = 'i-0c32153096cd68a6d'

        self.response = {
            'SessionId': 'session-020bf6cd31f912b53',
            'TokenValue': 'randomtokenvalue'
        }

    def test_create_session(self):
        with patch.object(self.ssm, 'start_session', return_value=self.response):
            sess = Session(instance_id=self.instance_id, ssm=self.ssm)
            sess.create()

            self.assertTrue(self.ssm.start_session.called)

    def test_terminate_session(self):
        with patch.object(self.ssm, 'terminate_session', return_value=self.response):
            sess = Session(instance_id=self.instance_id, ssm=self.ssm)

            sess.create()
            sess.terminate()

            self.assertTrue(self.ssm.terminate_session.called)

    def test_open_session(self):
        mock_output = MagicMock(stdout=b'output')

        with patch('aws_gate.session.execute', return_value=mock_output) as m:
            sess = Session(instance_id=self.instance_id, ssm=self.ssm)
            sess.open()

            self.assertTrue(m.called)

    def test_open_session_exception(self):
        with patch('aws_gate.session.execute',
                   side_effect=OSError(errno.ENOENT, os.strerror(errno.ENOENT))):
            with self.assertRaises(ValueError):
                sess = Session(instance_id=self.instance_id, ssm=self.ssm)
                sess.open()

    def test_context_manager(self):
        with patch.object(self.ssm, 'start_session', return_value=self.response) as sm, \
                patch.object(self.ssm, 'terminate_session', return_value=self.response) as tm:
            with Session(instance_id=self.instance_id, ssm=self.ssm):
                pass

            self.assertTrue(sm.called)
            self.assertTrue(tm.called)

    def test_session(self):
        with patch('aws_gate.session.get_aws_client', return_value=MagicMock()), \
                patch('aws_gate.session.get_aws_resource', return_value=MagicMock()), \
                patch('aws_gate.session.query_instance', return_value=self.instance_id), \
                patch('aws_gate.session.Session', return_value=MagicMock()) as session_mock, \
                patch('aws_gate.session.is_existing_profile', return_value=True), \
                patch('aws_gate.decorators._plugin_exists', return_value=True), \
                patch('aws_gate.decorators.execute', return_value='1.1.23.0'):
            session(config=self.config, instance_name=self.instance_id)
            self.assertTrue(session_mock.called)

    def test_session_exception_invalid_profile(self):
        with patch('aws_gate.session.get_aws_client', return_value=MagicMock()), \
                patch('aws_gate.session.get_aws_resource', return_value=MagicMock()), \
                patch('aws_gate.session.query_instance', return_value=None), \
                patch('aws_gate.decorators._plugin_exists', return_value=True), \
                patch('aws_gate.decorators.execute', return_value='1.1.23.0'):
            with self.assertRaises(ValueError):
                session(config=self.config, profile_name='invalid-profile', instance_name=self.instance_id)

    def test_session_exception_invalid_region(self):
        with patch('aws_gate.session.get_aws_client', return_value=MagicMock()), \
                patch('aws_gate.session.get_aws_resource', return_value=MagicMock()), \
                patch('aws_gate.session.query_instance', return_value=None), \
                patch('aws_gate.decorators._plugin_exists', return_value=True), \
                patch('aws_gate.decorators.execute', return_value='1.1.23.0'):
            with self.assertRaises(ValueError):
                session(config=self.config, region_name='invalid-region', instance_name=self.instance_id)

    def test_session_exception_unknown_instance_id(self):
        with patch('aws_gate.session.get_aws_client', return_value=MagicMock()), \
                patch('aws_gate.session.get_aws_resource', return_value=MagicMock()), \
                patch('aws_gate.session.query_instance', return_value=None), \
                patch('aws_gate.decorators._plugin_exists', return_value=True), \
                patch('aws_gate.decorators.execute', return_value='1.1.23.0'):
            with self.assertRaises(ValueError):
                session(config=self.config, instance_name=self.instance_id)

    def test_session_without_config(self):
        with patch('aws_gate.session.get_aws_client', return_value=MagicMock()), \
                patch('aws_gate.session.get_aws_resource', return_value=MagicMock()), \
                patch('aws_gate.session.query_instance', return_value=None), \
                patch('aws_gate.decorators._plugin_exists', return_value=True), \
                patch('aws_gate.decorators.execute', return_value='1.1.23.0'):
            with self.assertRaises(ValueError):
                session(config=self.empty_config, instance_name=self.instance_id)
