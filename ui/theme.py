from kivy.app import App
from kivy.clock import mainthread
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.properties import ColorProperty, OptionProperty, ObjectProperty


class ThemeManager(EventDispatcher):
    """
    Manages and applies theme configurations for a GUI application.

    The ThemeManager class is responsible for storing and managing various color
    and style properties of the application's graphical user interface. It allows
    switching between light and dark theme styles, updates relevant UI components
    accordingly, and supports customization of colors for background, text, shadows,
    cards, accents, and more. This provides a centralized theme management system
    for consistent application styling.

    :ivar bg_color: The current background color of the theme.
    :type bg_color: ColorProperty
    :ivar bg_color_light: The background color for the light theme.
    :type bg_color_light: ColorProperty
    :ivar bg_color_dark: The background color for the dark theme.
    :type bg_color_dark: ColorProperty
    :ivar card_color: The current card color of the theme.
    :type card_color: ColorProperty
    :ivar card_color_light: The card color for the light theme.
    :type card_color_light: ColorProperty
    :ivar card_color_dark: The card color for the dark theme.
    :type card_color_dark: ColorProperty
    :ivar primary_color: The current primary color of the theme.
    :type primary_color: ColorProperty
    :ivar primary_color_light: The primary color for the light theme.
    :type primary_color_light: ColorProperty
    :ivar primary_color_dark: The primary color for the dark theme.
    :type primary_color_dark: ColorProperty
    :ivar secondary_color: The current secondary color of the theme.
    :type secondary_color: ColorProperty
    :ivar secondary_color_light: The secondary color for the light theme.
    :type secondary_color_light: ColorProperty
    :ivar secondary_color_dark: The secondary color for the dark theme.
    :type secondary_color_dark: ColorProperty
    :ivar accent_color: The current accent color of the theme.
    :type accent_color: ColorProperty
    :ivar accent_color_light: The accent color for the light theme.
    :type accent_color_light: ColorProperty
    :ivar accent_color_dark: The accent color for the dark theme.
    :type accent_color_dark: ColorProperty
    :ivar shadow_color: The current shadow color of the theme.
    :type shadow_color: ColorProperty
    :ivar shadow_color_light: The shadow color for the light theme.
    :type shadow_color_light: ColorProperty
    :ivar shadow_color_dark: The shadow color for the dark theme.
    :type shadow_color_dark: ColorProperty
    :ivar text_color: The current text color of the theme.
    :type text_color: ColorProperty
    :ivar text_color_light: The text color for the light theme.
    :type text_color_light: ColorProperty
    :ivar text_color_dark: The text color for the dark theme.
    :type text_color_dark: ColorProperty
    :ivar transparent_color: The transparent color used in the theme.
    :type transparent_color: ColorProperty
    :ivar disabled_color: The color for disabled UI elements.
    :type disabled_color: ColorProperty
    :ivar theme_style: The current theme style, either "Light" or "Dark".
    :type theme_style: OptionProperty
    """
    bg_color = ColorProperty()
    bg_color_light = ColorProperty("white")
    bg_color_dark = ColorProperty("black")
    card_color = ColorProperty()
    card_color_light = ColorProperty("white")
    card_color_dark = ColorProperty("#black")
    primary_color = ColorProperty()
    primary_color_light = ColorProperty("black")
    primary_color_dark = ColorProperty("white")
    secondary_color = ColorProperty()
    secondary_color_light = ColorProperty()
    secondary_color_dark = ColorProperty()
    accent_color = ColorProperty()
    accent_color_light = ColorProperty([0, 0, 0, .05])
    accent_color_dark = ColorProperty([1, 1, 1, .08])
    shadow_color = ColorProperty()
    shadow_color_light = ColorProperty([0, 0, 0, .65])
    shadow_color_dark = ColorProperty([1, 1, 1, .65])
    text_color = ColorProperty()
    text_color_light = ColorProperty("#3F3F41")
    text_color_dark = ColorProperty("#FFFFFF")
    transparent_color = ColorProperty("#00000000")
    disabled_color = ColorProperty([.4, .4, .4, .7])
    theme_style = OptionProperty("Light", options=["Light", "Dark"])

    def __init__(self, *args, **kwargs):
        """
        Initializes the object and invokes the `on_theme_style` method after initialization.

        The initial setup process is carried out by calling the parent class's initializer
        with any provided arguments or keyword arguments. Once initialized, the object's
        `on_theme_style` method is executed to configure or apply additional styles or customization.

        :param args: Positional arguments to be passed to the parent class initializer.
        :type args: tuple
        :param kwargs: Keyword arguments to be passed to the parent class initializer.
        :type kwargs: dict
        """
        super().__init__(*args, **kwargs)
        self.on_theme_style()

    @mainthread
    def on_theme_style(self, *_):
        """
        The on_theme_style method is a callback designed to respond to changes in
        the theme style of the application. This method ensures that the theme is
        updated dynamically by calling the set_theme method whenever the theme style
        is modified. This function is intended to handle signals or events related
        to changes in the style theme.

        :param _: Arguments passed to the callback, typically ignored in this implementation.
        :return: None
        """
        self.set_theme()

    def set_theme(self, *_):
        """
        Updates the theme of the application based on the current theme style.

        This method adjusts various theme-related attributes, such as background color,
        primary color, secondary color, accent color, text color, shadow color, and card color
        according to the current `theme_style`. Additionally, it updates the application window's
        clear color and viewport to reflect the changes made in theme attributes.

        It distinguishes between two themes, 'Light' and other themes (assumed to be 'Dark'),
        assigning the corresponding colors based on the selected theme.

        :param _: Accepts any arguments, though they are unused within the method.
        :return: None
        """
        if self.theme_style == "Light":
            self.bg_color = self.bg_color_light
            self.primary_color = self.primary_color_light
            self.secondary_color = self.secondary_color_light
            self.accent_color = self.accent_color_light
            self.text_color = self.text_color_light
            self.shadow_color = self.shadow_color_light
            self.card_color = self.card_color_light
        else:
            self.bg_color = self.bg_color_dark
            self.primary_color = self.primary_color_dark
            self.secondary_color = self.secondary_color_dark
            self.accent_color = self.accent_color_dark
            self.text_color = self.text_color_dark
            self.shadow_color = self.shadow_color_dark
            self.card_color = self.card_color_dark

        Window.clearcolor = self.bg_color
        Window.update_viewport()


class Theme:
    """
    Represents a theme management class for a UI application.

    The `Theme` class is designed to provide access and management of the application's
    theme via the `theme_cls` object property. It initializes the `theme_cls` with the
    current running application's theme object and inherits additional properties and
    behaviors from its superclass.

    :ivar theme_cls: The theme object property for the running application.
    :type theme_cls: ObjectProperty
    """
    theme_cls = ObjectProperty()

    def __init__(self, *args, **kwargs):
        self.theme_cls = App.get_running_app().theme_cls
        super().__init__(*args, **kwargs)
