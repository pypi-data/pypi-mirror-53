from unittest import TestCase
from unittest import mock

from busy.bash import Bash
from busy.root.file_system_root import FilesystemRoot
from busy.root.dropbox_root import DropboxRoot

class TestBash(TestCase):

    def test_commands(self):
        b = Bash('a','b')
        self.assertEqual(b.commands, ['a','b'])

    def test_default_storage(self):
        b = Bash('a','b')
        self.assertIsInstance(b.root, FilesystemRoot)

    def test_dropbox_storage_commands(self):
        with mock.patch('busy.root.dropbox_root.dropbox_token','x'):
            b = Bash('--dropbox','a','b')
            self.assertEqual(b.commands, ['a','b'])

    def test_dropbox_storage_root(self):
        with mock.patch('busy.root.dropbox_root.dropbox_token','x'):
            b = Bash('--dropbox','a','b')
            self.assertIsInstance(b.root, DropboxRoot)

    def test_optional_args_persist(self):
        with mock.patch('busy.root.dropbox_root.dropbox_token','x'):
            b = Bash('--dropbox','a','--b','c')
            self.assertEqual(b.commands, ['a', '--b', 'c'])
