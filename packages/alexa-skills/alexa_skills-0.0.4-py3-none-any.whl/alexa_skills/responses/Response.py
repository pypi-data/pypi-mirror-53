class Response:

    def __init__(self):
        self._output_speech = None
        self._card = None
        self._reprompt = None
        self._directives = []
        self._should_end_session = False

    def set_output_speech(self, output_speech):
        self._output_speech = output_speech

    def set_card(self, card):
        self._card = card

    def set_reprompt(self, reprompt):
        self._reprompt = reprompt

    def add_directive(self, directive):
        self._directives.append(directive)

    def set_should_end_session(self, should_end_session):
        self._should_end_session = should_end_session

    def build(self):
        response = {}

        if self._output_speech:
            response["outputSpeech"] = self._output_speech.build()

        if self._reprompt:
            response["reprompt"] = self._reprompt.build()

        if self._card:
            response["card"] = self._card.build()

        if self._directives:
            response["directives"] = [directive.build() for directive in self._directives]

        response["shouldEndSession"] = self._should_end_session

        return response
