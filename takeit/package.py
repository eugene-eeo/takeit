from uritemplate import expand


class Package(object):
    QUERY_URL = 'https://cdnjs.com/libraries{/id}{/version}'

    def __init__(self, id, version):
        self.id = id
        self.version = version
        self.files = None

    @property
    def url(self):
        return expand(self.QUERY_URL,
                      id=self.id,
                      version=self.version)

    @classmethod
    def from_string(cls, string):
        parts = string.split('==', 1)
        if len(parts) == 1:
            parts.append(None)
        return cls(*parts)
