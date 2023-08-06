import json


class Dialog:

    def __init__(self, updated_intent):
        self._type = "Dialog.Delegate"
        self._updated_intent = json.loads(json.dumps(
            updated_intent,
            default=lambda x: getattr(x, '__dict__', str(x))
        ))

    def build(self):
        return {
            "type": self._type,
            "updatedIntent": self._updated_intent
        }
