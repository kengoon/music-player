from kivy.core.text import LabelBase
from kivy.loader import Loader
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy_reloader.app import App
from kivy import platform
from components.factory_register import register_factory
from components.transition import SharedAxisTransition
from features.screenmanager import AppScreenManager
from ui.theme import ThemeManager

LabelBase.register(
    "Roboto",
    'assets/fonts/Poppins-Regular.ttf',
    'assets/fonts/Poppins-Italic.ttf',
    'assets/fonts/Poppins-SemiBold.ttf',
    'assets/fonts/Poppins-SemiBoldItalic.ttf'
)
Loader.error_image = "assets/images/transparent.png"
Loader.loading_image = "assets/images/transparent.png"
register_factory()

if platform == "android":
    """
    This block is executed only when the application is running on an Android platform.

    1. It imports the set_edge_to_edge function from the kvdroid.tools.display module.
    2. The set_edge_to_edge() function is called to configure the application's edge-to-edge display layout. 
       This layout setup allows the application content to extend to the full screen, 
       including areas under system bars (status bar and navigation bar), in compliance with Android UI guidelines.
    """
    from kvdroid.tools.display import set_edge_to_edge

    set_edge_to_edge()


class MusicPlayerApp(App):
    """
    MusicPlayerApp class.

    This class represents a Music Player Application. It utilizes Kivy for building the
    graphical user interface and provides features such as theme management and platform-specific
    adjustments for status bar and navbar heights on Android. The primary functionality of the class
    is to initialize and configure the application layout and behavior, ensuring seamless integration
    with the underlying platform.

    :ivar theme_cls: Theme management object used for handling theme styling within the application.
    :type theme_cls: ThemeManager
    :ivar use_kivy_settings: Boolean flag indicating whether Kivy settings should be used.
    :type use_kivy_settings: bool
    :ivar kv_file: Path to the KV file defining the application's layout.
    :type kv_file: StringProperty
    :ivar statusbar_height: Height of the device's status bar. This value is specific to the Android platform.
    :type statusbar_height: NumericProperty
    :ivar navbar_height: Height of the device's navigation bar. This value is specific to the Android platform.
    :type navbar_height: NumericProperty
    """
    theme_cls = ObjectProperty()
    use_kivy_settings = False
    kv_file = StringProperty("imports.kv")
    if platform == "android":
        from kvdroid.tools.display import get_statusbar_height, get_navbar_height
        statusbar_height = NumericProperty(get_statusbar_height())
        navbar_height = NumericProperty(get_navbar_height())
    else:
        statusbar_height = NumericProperty(0)
        navbar_height = NumericProperty(0)

    def __init__(self, **kwargs):
        """
        Initializes the application with specified keyword arguments and configures
        the theme and color settings for the status bar and navigation bar. This setup
        ensures that the visual appearance aligns with the theme style, adapting to
        light or dark modes when necessary. Special handling is included for Android
        platform-specific requirements.

        :param kwargs: Keyword arguments passed to the initializer. These arguments
            are supplied to the parent class' initializer method.
        :raises ImportError: Raised when necessary modules for Android platform
            adjustments are not available.
        """
        super().__init__(**kwargs)
        self.sm = None
        self.theme_cls = ThemeManager()
        # self.theme_cls.theme_style = "Dark"
        if platform == "android":
            from kvdroid.tools import change_statusbar_color, navbar_color
            change_statusbar_color(
                [0, 0, 0, 0],
                "black" if self.theme_cls.theme_style == "Light" else "white"
            )
            navbar_color(
                [0, 0, 0, 0],
                "black" if self.theme_cls.theme_style == "Light" else "white"
            )
            self.theme_cls.bind(
                bg_color=lambda _, value: (
                    change_statusbar_color(
                        [0, 0, 0, 0],
                        "black" if self.theme_cls.theme_style == "Light" else "white"
                    ),
                    navbar_color(
                        [0, 0, 0, 0],
                        "black" if self.theme_cls.theme_style == "Light" else "white"
                    )
                )
            )

    def build(self):
        """
        Builds and configures the main application layout and screen manager, along with
        navigation and padding adjustments for different platform behaviors.

        This method creates the main user interface setup for the application. It adds
        the `AppScreenManager` widget to a `BoxLayout`, which serves as the container
        for the app screens. On Android, it binds the `current` property of the screen
        manager to dynamically adjust padding based on the current screen name.

        :rtype: BoxLayout
        :return: The fully configured root layout for the application, including the
            screen manager and platform-specific behavior configurations.
        """
        self.sm = AppScreenManager(transition=SharedAxisTransition())
        box = BoxLayout()
        box.add_widget(self.sm)
        if platform == "android":
            self.sm.bind(
                current=lambda _, name: (
                    setattr(box, "padding", [0, self.statusbar_height, 0, self.navbar_height])
                    if name != "player screen" else
                    setattr(box, "padding", [0, 0, 0, 0])
                )
            )
        self.sm.current = "player screen"
        return box


if __name__ == '__main__':
    import trio

    app = MusicPlayerApp()
    trio.run(app.async_run, "trio")
