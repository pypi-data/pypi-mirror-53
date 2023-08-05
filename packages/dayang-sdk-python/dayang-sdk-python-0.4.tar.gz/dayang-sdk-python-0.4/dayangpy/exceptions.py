class BaseException(Exception):
    def __init__(self, text):
        self.text = str(text)

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text
