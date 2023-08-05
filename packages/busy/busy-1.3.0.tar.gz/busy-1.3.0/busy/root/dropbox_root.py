import http.client
import os

from . import Root

HTTPSConnection = http.client.HTTPSConnection
dropbox_token = os.environ.get('DROPBOX_TOKEN')


class DropboxRoot(Root):

    def __init__(self):
        assert dropbox_token
        super().__init__()

    def _read(self, key):
        c = HTTPSConnection("content.dropboxapi.com")
        h = {
            'Authorization': f"Bearer {dropbox_token}",
            'Dropbox-API-Arg': f'{{"path": "/{key}.txt"}}'
        }
        c.request("POST", "/2/files/download", headers=h)
        r = c.getresponse()
        if r.status == 200:
            return [i.strip() for i in r.read().decode("utf-8").split('\n')]

    def _save(self, key, items):
        c = HTTPSConnection("content.dropboxapi.com")
        h = {
            'Authorization': f"Bearer {dropbox_token}",
            'Dropbox-API-Arg': f'{{"path": "/{key}.txt"}}',
            'Content-Type': 'application/octet-stream'
        }
        body = "\n".join(str(i) for i in items)
        c.request("POST", "/2/files/upload", headers=h, body=body)
