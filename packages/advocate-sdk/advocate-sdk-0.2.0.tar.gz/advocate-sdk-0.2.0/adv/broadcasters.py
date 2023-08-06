class Broadcaster:
    def __init__(self, client, name='', id=None):
        self.client = client

        self.name = name
        self.id = id

    def __repr__(self):
        return '<BROADCASTER: {}>'.format(self)

    def __str__(self):
        return self.name
