import sys
from conversion_predictor.Connector import TaboolaConnector
from conversion_predictor.TokenRefresher import TaboolaTokenRefresher
from pydoc import locate
import importlib
from abc import ABC, abstractmethod


class Factory(ABC):

    def __init__(self, type):
        """
        Constructor for the Factory class. Takes the type of factory required for use in other methods.
        """
        self.type = type
        sys.path.append('C:\\Users\\Kathryn\\PycharmProjects\\taboola-conversion-predictor\\conversion_predictor')

    def get_object(self, platform):
        """
        Gets the required object as specified by the type and platform combination.
        :param platform:
        :return: an instance of the class
        """
        try:
            obj = self.get_class_name(platform)
            return obj()
        except AttributeError:
            raise

    def get_class_name(self, platform):
        """
        Gets the required class name as specified by the type and platform combination.
        :param platform:
        :return:
        """
        try:
            module = importlib.import_module(self.type)
            my_class = getattr(module, platform + self.type)
            return my_class
        except AttributeError:
            raise


class ConnectorFactory(Factory):
    """
    Class representing a factory of type Connector.
    """

    def __init__(self):
        super().__init__('Connector')

    def get_object(self, platform):
        return super().get_object(platform)

    def get_class_name(self, platform):
        return super().get_class_name(platform)


class TokenRefresherFactory(Factory):
    """
    Class representing a factory of type TokenRefresher.
    """

    def __init__(self):
        super().__init__('TokenRefresher')

    def get_object(self, platform):
        return super().get_object(platform)

    def get_class_name(self, platform):
        return super().get_class_name(platform)
