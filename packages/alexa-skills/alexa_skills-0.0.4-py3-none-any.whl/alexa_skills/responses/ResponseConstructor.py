from alexa_skills.responses.OutputSpeech import OutputSpeech
from alexa_skills.responses.Reprompt import Reprompt
from alexa_skills.responses.Response import Response


class ResponseConstructor:

    def __init__(self):
        self._response = Response()

    def speak(self, text):
        """
        Sets output speech for response

        :param text: (string)
        :return: (ResponseConstructor)
        """

        self._response.set_output_speech(OutputSpeech(text))
        return self

    def ask(self, reprompt):
        """
        Sets reprompt speech for response

        :param reprompt: (string)
        :return: (ResponseConstructor)
        """

        self._response.set_reprompt(Reprompt(reprompt))
        return self

    def set_card(self, card):
        """
        Sets card for response

        :param card: (Card)
        :return: (ResponseConstructor)
        """

        self._response.set_card(card)
        return self

    def add_directive(self, directive):
        """
        Adds a new directive to the directives list

        :param directive: (AbstractDirective)
        :return: (ResponseConstructor)
        """

        self._response.add_directive(directive)
        return self

    def set_should_end_session(self, should_end_session):
        """
        Sets should_end_session

        :param should_end_session: (boolean)
        :return: (ResponseConstructor)
        """

        self._response.set_should_end_session(should_end_session)
        return self

    def build(self):
        """
        Builds the response using response build method

        :return: (dict)
        """

        return self._response.build()
