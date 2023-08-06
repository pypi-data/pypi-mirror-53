class Card:

    def __init__(self, title, content):
        self._type = "Simple"
        self._title = title
        self._content = content

    def build(self):
        return {
            "type": self._type,
            "title": self._title,
            "content": self._content
        }