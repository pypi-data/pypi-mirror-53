from alexa_skills.requests.HandlerInput import HandlerInput
from alexa_skills.session.SessionManager import SessionManager


class RequestHandler:

    def __init__(self, request, context):
        """
        RequestHandler Constructor

        :param request: request / event object from lamdba handler (object)
        :param context: lambda handler context (object)
        """

        self._handler_input = HandlerInput(
            request=request.request,
            context=request.context,
            session_manager=SessionManager(request.session)
        )

        self._context = context

    def _get_handler(self, request_handlers):
        """
        Iterates through request handlers, when a successful request handler is found then

        :param request_handlers: (list)
        :return: (handler)
        """

        for handler in request_handlers:
            if handler.can_handle(self._handler_input):
                return handler

    def handle(self, request_handlers):
        """
        Handles request according to request handlers

        :param request_handlers: (list)
        :return: (ResponseConstructor)
        """

        handler = self._get_handler(request_handlers)
        try:
            handler.handle(self._handler_input)
        except Exception as error:
            handler.handle_error(self._handler_input, error)

        return self._handler_input
