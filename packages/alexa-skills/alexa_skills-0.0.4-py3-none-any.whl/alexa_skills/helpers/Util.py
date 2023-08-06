from alexa_skills.helpers.Constants import NON_PRIMATIVES


class Struct:

    def __init__(self, dictionary):
        """
        Converts Python dictionary to object, if nested non-primative types are in the object then they are converted
        as well using recursion

        :param dictionary: (dict)
        """

        for key, value in dictionary.items():
            setattr(self, key, self._struct(value))

    def _struct(self, value):
        """
        Struct wrapper, recursive method for converting values.

        :param value: (!= dict)
        :return:
        """

        if isinstance(value, NON_PRIMATIVES):
            return type(value)([
                self._struct(item) for item in value
            ])

        return Struct(value) if isinstance(value, dict) else value


def is_dialog_complete(handler_input):
    """
    Checks whether the dialog is complete according to the dialog model

    :param handler_input: (HandlerInput)
    :return: (boolean)
    """

    if not hasattr(handler_input.get_request(), "dialogState"):
        return False

    return handler_input.get_request().dialogState == "COMPLETE"


def is_request_type(request_type):
    """
    Constructs a function that returns True when request type is equal to :param request_type.

    :param request_type: (string)
    :return: (callable)
    """

    def wrapper(hander_input):
        """
        Function that returns True when request type is equal to request_type

        :param hander_input: (HandlerInput)
        :return: (boolean)
        """

        return hander_input.get_request().type == request_type

    return wrapper


def is_intent(intent_name):
    """
    Constructs a function that returns True when intent name is equal to :param intent_name.

    :param intent_name: (string)
    :return: (callable)
    """

    def wrapper(handler_input):
        """
        Function that returns True when intent name is equal to intent_name

        :param handler_input: (HandlerInput)
        :return: (boolean)
        """

        return is_request_type("IntentRequest")(handler_input) and handler_input.get_request().intent.name == intent_name

    return wrapper

