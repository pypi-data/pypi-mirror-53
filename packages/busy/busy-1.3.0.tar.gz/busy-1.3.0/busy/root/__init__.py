
from ..queue import Queue


class Root:

    def __init__(self):
        self._queues = {}

    def _read(self, key):
        return ""

    def get_queue(self, key=None):
        key = key or Queue.default_key
        queueclass = Queue.subclass(key)
        lines = self._read(key)
        self._queues[key] = queueclass(self, lines)
        return self._queues[key]

    def _save(self, key, items):  # pragma: no cover
        pass

    def save(self):
        while self._queues:
            key, queue = self._queues.popitem()
            if queue.changed:
                items = queue.all()
                self._save(key, items)
