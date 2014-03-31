class Session(object):
    def __init__(self, sdk, session_id, **kwargs):
        self.session_id = session_id
        self.sdk = sdk
        for key, value in kwargs.items():
            setattr(self, key, value)

    def generate_token(self, **kwargs):
        return self.sdk.generate_token(self.session_id, **kwargs)
