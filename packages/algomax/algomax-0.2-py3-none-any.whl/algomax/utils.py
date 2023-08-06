import json


def get_config(filename: str):
    """
    load data from json file
    :param filename: path of json file
    :return: dict contains data of the json file
    """
    with open(filename, 'r') as file_reader:
        config = json.loads(file_reader.read())

    return config


class BColor:
    """
    colors for cli result text
    """

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def success(message: str):
        """
        get a text and return it with green color
        :param message: an input message
        :return: green color text
        """

        return '{0}{1}{2}'.format(BColor.OKGREEN, message, BColor.ENDC)

    @staticmethod
    def failed(message: str):
        """
        get a text and return it with red color
        :param message: an input message
        :return: red color text
        """
        return '{0}{1}{2}'.format(BColor.FAIL, message, BColor.ENDC)

    @staticmethod
    def info(message: str):
        """
        get a text and return it with blue color
        :param message: an input message
        :return: blue color text
        """
        return '{0}{1}{2}'.format(BColor.OKBLUE, message, BColor.ENDC)

    @staticmethod
    def bold(message: str):
        """
        get a text and return it with bold style
        :param message: an input message
        :return: bold style text
        """
        return '{0}{1}{2}'.format(BColor.BOLD, message, BColor.ENDC)
