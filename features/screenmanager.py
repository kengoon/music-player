from kivy import platform
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import DictProperty
from kivy.uix.screenmanager import ScreenManager
from importlib import import_module
from components.bar import win_md_bnb


class AppScreenManager(ScreenManager):
    """
    Manages the application's navigation and dynamic screen loading.

    The AppScreenManager class extends the ScreenManager to provide custom screen
    handling functionality. It enables lazy loading of screens based on the app's
    current state, ensuring efficient resource usage. It also includes keyboard
    event handling for navigation, specifically designed for Android environments.

    :ivar screen_config: A dictionary mapping screen names to their presentation
         module paths and class names.
    :type screen_config: dict
    """
    screen_config = DictProperty(
        {
            "player screen": {
                "presentation": ("features.player.presentation", "PlayerScreen")
            },
        }
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self._go_back)

    def on_current(self, instance, value):
        """
        Handles the operations to perform when the current screen changes in the
        application. It ensures that the correct screen is displayed, and the
        necessary presentation is dynamically loaded if required.

        This method validates whether the requested screen is available. If not, it dynamically
        loads the corresponding presentation module and initializes it. Additionally, it manages
        the application's screen transitions and widget hierarchy.

        :param instance: The instance that triggered the `on_current` event.
        :type instance: Any
        :param value: The name of the current screen to navigate to.
        :type value: str
        :return: The result of the parent class's `on_current` method after executing this logic.
        :rtype: Any
        """
        if value in ["login screen", "signup screen"] and win_md_bnb.bar:
            win_md_bnb.pop()
        if not self.has_screen(value):
            screen_data = self.screen_config[value]
            presentation_module_path, presentation_class_name = screen_data["presentation"]
            presentation_module = import_module(presentation_module_path)
            presentation_class = getattr(presentation_module, presentation_class_name)
            presentation = presentation_class()
            presentation.app = App.get_running_app()
            self.add_widget(presentation)
        supra = super().on_current(instance, value)
        # if len(self.children) > 1:
        #     self.remove_widget(self.children[1])
        return supra

    def _go_back(self, _window, key, *_args):
        """
        Handles the "go back" action in the application.

        This method is triggered when a specific key event occurs, allowing the application
        to navigate back to the previous screen or perform platform-specific actions in
        certain cases. It checks if the current screen is the first in the sequence and,
        if the platform is Android, sends the task to the background. Otherwise, it
        switches to the previous screen and updates the relevant components.

        :param _window: The current window instance (unused in the function).
        :param key: The key code for the triggering event.
        :param _args: Additional positional arguments (unused in the function).
        :return: A boolean indicating whether the operation succeeded.
        """
        if key == 1073742106:
            if self.screens.index(self.current_screen) == 0 and platform == "android":
                from android import mActivity
                mActivity.moveTaskToBack(True)
                return True
            self.current = self.previous()
            for child in win_md_bnb.bar.children:
                if self.current == child.name:
                    child.dispatch("on_release")
            return True

