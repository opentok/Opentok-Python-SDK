class Session(object):
    def __init__(self, session_id, **kwargs):
        self.session_id = session_id
        for key, value in kwargs.items():
            setattr(self, key, value)
