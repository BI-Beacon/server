class StateServer(object):
    def __init__(self, db):
        self.db = db

    def __getitem__(self, name):
        return self.db[name]
