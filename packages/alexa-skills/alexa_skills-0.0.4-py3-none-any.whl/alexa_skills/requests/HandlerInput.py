from alexa_skills.responses.ResponseConstructor import ResponseConstructor


class HandlerInput:

    def __init__(self, request, context, session_manager):
        """
        HandlerInput constructor

        :param request: request object from the lambda event (object)
        :param context: context object from the lambda event (object)
        :param session_manager: (SessionManager)
        """

        self._request = request
        self._context = context
        self._session_manager = session_manager
        self._response_constructor = ResponseConstructor()

    def get_request(self):
        """
        Fetches private request object

        :return: (Object)
        """

        return self._request

    def get_context(self):
        """
        Fetches private context object

        :return: (Object)
        """

        return self._context

    def get_session_manager(self):
        """
        Fetches private session manager object

        :return: (Object)
        """

        return self._session_manager

    def get_response_constructor(self):
        """
        Fetches private response constructor object

        :return: (Object)
        """

        return self._response_constructor

    def build_response(self):
        """
        Builds the response using the session manager attributes and response constructor

        :return: (dict)
        """

        return {
            "version": "1.0",
            "sessionAttributes": self._session_manager.get_session_attributes(),
            "response": self._response_constructor.build()
        }
