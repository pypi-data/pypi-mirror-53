from abc import ABC as Abstract, abstractmethod


class AbstractRequestHandler(Abstract):

    @abstractmethod
    def can_handle(self, handler_input):
        """
        Returns True if Request Handler can handle the Request inside the
        :param: handler_input

        :param handler_input: (HandlerInput)
        :return: (boolean)
        """

        pass

    @abstractmethod
    def handle_error(self, handler_input, error):
        """
        Returns response if an error occurs

        :param handler_input: (HandlerInput)
        :param error: (Exception)
        :return: (Response)
        """

        pass

    @abstractmethod
    def handle(self, handler_input):
        """
        Returns response from handler

        :param handler_input: (HandlerInput)
        :return: (Response)
        """

        pass
