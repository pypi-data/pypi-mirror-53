from copy import deepcopy
import json

class EmptySessionAttributes:
    pass


class SessionManager:

    def __init__(self, session):
        self._session = session

        if hasattr(self._session, "attributes"):
            self._session_attributes = deepcopy(self._session.attributes)
        else:
            self._session_attributes = EmptySessionAttributes()

    def get_session(self):
        return self._session

    def get_session_attributes(self):
        return json.loads(json.dumps(
            self._session_attributes,
            default=lambda x: getattr(x, '__dict__', str(x))
        ))

    def get_session_attribute(self, key):
        if not hasattr(self._session_attributes, key):
            return None

        return getattr(self._session_attributes, key)

    def set_session_attribute(self, key, value):
        setattr(self._session_attributes, key, value)