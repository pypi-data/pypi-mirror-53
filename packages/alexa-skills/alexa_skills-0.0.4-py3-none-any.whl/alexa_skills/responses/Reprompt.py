class Reprompt:

    def __init__(self, text):
        self._type = "PlainText"
        self._text = text

    def build(self):
        return {
            "outputSpeech": {
                "type": self._type,
                "text": self._text
            }
        }