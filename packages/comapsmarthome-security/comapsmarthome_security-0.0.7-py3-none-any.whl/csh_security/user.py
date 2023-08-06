import os


class User:
    def __init__(self, id, roles):
        self.id = id
        self.roles = roles

    def is_local(self):
        return self.id == 'johndoe' and os.environ.get('IS_LOCAL', 'false') == 'true'
