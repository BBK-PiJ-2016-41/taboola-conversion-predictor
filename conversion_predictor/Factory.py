import sys
from conversion_predictor.Connector import TaboolaConnector
from conversion_predictor.TokenRefresher import TaboolaTokenRefresher
from abc import ABC, abstractmethod


class Factory(ABC):

    def __init__(self, type):
        """
        Constructor for the Factory class. Takes the type of factory required for use in other methods.
        :param type:
        """
        self.type = type

    @abstractmethod
    def get_object(self, platform):
        """
        Gets the required object as specified by the type and platform combination.
        :param platform:
        :return:
        """
        try:
            class_name = self.get_class_name(platform)
        except AttributeError:
            raise

        return class_name()

    @abstractmethod
    def get_class_name(self, platform):
        """
        Gets the required class name as specified by the type and platform combination.
        :param platform:
        :return:
        """
        try:
            return getattr(sys.modules[__name__], platform + self.type)
        except AttributeError:
            raise


class ConnectorFactory(Factory):

    def __init__(self):
        super().__init__('Connnector')

    def get_object(self, platform):
        super().get_object(platform)

    def get_class_name(self, platform):
        super().get_class_name(platform)


class TokenRefresherFactory(Factory):

    def __init__(self):
        super().__init__('TokenRefresher')

    def get_object(self, platform):
        super().get_object(platform)

    def get_class_name(self, platform):
        super().get_class_name(platform)
