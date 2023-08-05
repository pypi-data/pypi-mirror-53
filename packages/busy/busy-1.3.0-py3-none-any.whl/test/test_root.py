from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import mock
from unittest.mock import MagicMock

from busy.plugins.todo import TodoQueue
from busy.root.file_system_root import FilesystemRoot
from busy.file import File
from busy.root.dropbox_root import DropboxRoot

class TestFilesystemRoot(TestCase):

    def test_root(self):
        with TemporaryDirectory() as d:
            sd = FilesystemRoot(Path(d))
            s = sd.get_queue('tasks')
            self.assertIsInstance(s, TodoQueue)

    def test_add_todo(self):
        with TemporaryDirectory() as td:
            sd1 = FilesystemRoot(Path(td))
            sd1.get_queue('x').add('a')
            sd1.save()
            sd2 = FilesystemRoot(Path(td))
            self.assertEqual(str(sd2.get_queue('x').get()),'a')

    def test_make_dir_pater(self):
        with TemporaryDirectory() as td:
            r = FilesystemRoot(Path(td))
            r.get_queue('y').add('a')
            r.save()
            r2 = FilesystemRoot(Path(td))
            self.assertEqual(str(r2.get_queue('y').get()),'a')

    def test_env_var_as_backup(self):
        with TemporaryDirectory() as td:
            with mock.patch.dict('os.environ', {'BUSY_ROOT': td}):
                sd1 = FilesystemRoot()
                sd1.get_queue('p').add('a')
                sd1.save()
                f = Path(td) / 'p.txt'
                self.assertEqual(f.read_text(),'a\n')

    def test_user_root(self):
        with TemporaryDirectory() as td:
            with mock.patch.dict('os.environ', clear=True):
                with mock.patch('pathlib.Path.home', lambda : Path(td)):
                    sd1 = FilesystemRoot()
                    sd1.get_queue('w').add('a')
                    sd1.save()
                    f = Path(td) / '.busy' / 'w.txt'
                    self.assertEqual(f.read_text(),'a\n')


class MockResponse():
    
    def __init__(self):
        self.status = 200

MockResponse.read = MagicMock(return_value=bytearray("2019-01-01|a",'utf-8'))


class MockConnection():

    def __init__(self, domain):
        pass

MockConnection.request = MagicMock()
MockConnection.getresponse = MagicMock(return_value=MockResponse())


class TestDropboxRoot(TestCase):

    def test_mock(self):
        c = MockConnection("")
        c.request("", "", headers={})
        r = c.getresponse()
        self.assertEqual(r.read().decode('utf-8'), '2019-01-01|a')
    
    def test_get_queue_outline(self):
        m = MockConnection
        with mock.patch('busy.root.dropbox_root.HTTPSConnection', m):
            with mock.patch('busy.root.dropbox_root.dropbox_token','x'):
                sd = DropboxRoot()
                s = sd.get_queue('tasks')
                t = s.get()
                self.assertEqual(str(t), '2019-01-01|a')
                m.request.assert_called_with('POST', '/2/files/download', headers={'Authorization': 'Bearer x', 'Dropbox-API-Arg': '{"path": "/tasks.txt"}'})

    def test_get_another_queue(self):
        m = MockConnection
        with mock.patch('busy.root.dropbox_root.HTTPSConnection', m):
            with mock.patch('busy.root.dropbox_root.dropbox_token','x'):
                sd = DropboxRoot()
                s = sd.get_queue('z')
                s.get()
                m.request.assert_called_with('POST', '/2/files/download', headers={'Authorization': 'Bearer x', 'Dropbox-API-Arg': '{"path": "/z.txt"}'})

    def test_save(self):
        m = MockConnection
        with mock.patch('busy.root.dropbox_root.HTTPSConnection', m):
            with mock.patch('busy.root.dropbox_root.dropbox_token','x'):
                sd = DropboxRoot()
                s = sd.get_queue('z')
                s.add('a')
                sd.save()
                m.request.assert_called_with('POST','/2/files/upload', body='2019-01-01|a\na', headers={'Authorization': 'Bearer x', 'Dropbox-API-Arg': '{"path": "/z.txt"}', 'Content-Type': 'application/octet-stream'})
