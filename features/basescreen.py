from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from libs.singleton import screen_extras


class BaseScreen(Screen):
    """
    BaseScreen serves as a foundation for creating screen-based components with customizable
    data sources and app references.

    This class provides static utility methods to interact with a shared dictionary (`screen_extras`)
    to store, retrieve, and manage additional data without relying on instance-specific attributes. It
    aims to simplify data handling related to screens and their interactions with other components.

    :ivar data_source: Represents the data source property for the screen.
    :type data_source: Any
    :ivar app: Represents the app property related to the screen.
    :type app: Any
    """
    data_source = ObjectProperty(None)
    app = ObjectProperty(None)

    @staticmethod
    def toast(text, length_long=True):
        """
        Displays a toast message on Android devices using the KivyDroid library.

        This static method makes use of the `toast` function from the KivyDroid
        tools module to display a brief or long message overlay on the screen.
        Toasts are small popup messages typically used for showing notifications
        without requiring user interaction.

        :param text: The text message to display in the toast.
        :type text: str
        :param length_long: Determines the duration of the toast message.
            If True, the message is displayed for a long duration; otherwise,
            it is displayed for a short duration.
        :type length_long: bool
        :return: None
        """
        from kvdroid.tools import toast
        toast(text, length_long)

    @staticmethod
    def put_extra(key, value):
        """
        Adds an extra key-value pair to the global `screen_extras` dictionary.

        This method allows storing additional data in a central dictionary for further
        use or processing. The provided key is associated with the corresponding value
        to extend the functionality of the existing data structure. This method is
        static and does not depend on instance attributes.

        :param key: The key to be added to the dictionary.
        :type key: Any
        :param value: The value corresponding to the key to be added to the dictionary.
        :type value: Any
        :return: None
        """
        screen_extras[key] = value

    @staticmethod
    def get_extra(key, default=None):
        """
        Retrieve a value from a dictionary using a given key or return a default value.

        This method is a static utility that searches for a value associated with a specific
        key in the `screen_extras` dictionary. If the key does not exist in the dictionary,
        the method returns the provided default value. If no default value is provided,
        it defaults to `None`.

        :param key: The key used to locate the value in the `screen_extras` dictionary.
        :type key: Any
        :param default: The value returned if the key is not found. Defaults to None.
        :type default: Any, optional
        :return: The value associated with the key in the dictionary if the key exists;
                 otherwise, the default value.
        :rtype: Any
        """
        return screen_extras.get(key, default)

    @staticmethod
    def remove_extra(key):
        """
        Removes a specified key from the global dictionary `screen_extras`.

        Parameters
        ----------
        key :
            The key to be removed from the `screen_extras` dictionary.

        Returns
        -------
        None
            This method does not return any value.

        """
        del screen_extras[key]
