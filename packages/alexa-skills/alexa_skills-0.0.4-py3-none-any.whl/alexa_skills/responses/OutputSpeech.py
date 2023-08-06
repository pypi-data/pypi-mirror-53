class OutputSpeech:

    def __init__(self, text):
        self._type = "PlainText"
        self._text = text

    def build(self):
        return {
            "type": self._type,
            "text": self._text
        }