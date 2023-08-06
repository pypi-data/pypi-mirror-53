from alexa_skills.helpers.Util import Struct
from alexa_skills.requests.RequestHandler import RequestHandler


class Skill:

    def __init__(self):
        """
        Skill Constructor. Initializes the request handlers list
        """

        self._request_handlers = []

    def add_request_handler(self, request_handler):
        """
        Adds a request handler to the request handlers list

        :param request_handler: (AbstractRequestHandler)
        :return: (None)
        """

        self._request_handlers.append(request_handler())

    def lambda_handler(self):
        """
        Constructs lambda handler function.

        :return: (callable)
        """

        def handler(event, context):
            request_handler = RequestHandler(Struct(event), context)
            response = request_handler.handle(self._request_handlers)
            return response.build_response()

        return handler
