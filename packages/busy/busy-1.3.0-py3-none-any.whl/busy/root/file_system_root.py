from pathlib import Path
from tempfile import TemporaryDirectory
import os

from ..file import File
from ..queue import Queue
from . import Root


class FilesystemRoot(Root):

    def __init__(self, path=None):
        if path:
            self._path = Path(path) if isinstance(path, str) else path
            assert isinstance(self._path, Path) and self._path.is_dir()
        else:
            env_var = os.environ.get('BUSY_ROOT')
            self._path = Path(env_var if env_var else Path.home() / '.busy')
            if not self._path.is_dir():
                self._path.mkdir()
        self._files = {}
        self._queues = {}

    def get_queue(self, key=None):
        key = key or Queue.default_key
        if key not in self._queues:
            queueclass = Queue.subclass(key)
            queuefile = File(self._path / f'{key}.txt')
            self._files[key] = queuefile
            self._queues[key] = queueclass(self)
            self._queues[key].add(*queuefile.read(queueclass.itemclass))
        return self._queues[key]

    def _save(self, key, items):
        self._files[key].save(*items)
