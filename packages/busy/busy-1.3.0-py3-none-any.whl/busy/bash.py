from argparse import ArgumentParser

from .root.file_system_root import FilesystemRoot
from .root.dropbox_root import DropboxRoot

class Bash:
    
    def __init__(self, *input):
        self._parser = ArgumentParser()
        self._parser.add_argument('--dropbox', action='store_true')
        known, unknown = self._parser.parse_known_args(input)
        self.commands = unknown
        if known.dropbox:
            self.root = DropboxRoot()
        else:
            self.root = FilesystemRoot()

