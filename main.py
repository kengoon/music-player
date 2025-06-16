from kivy.core.text import LabelBase
from kivy.loader import Loader
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy_reloader.app import App
from kivy import platform

from components.bar import win_md_bnb
from components.factory_register import register_factory
from components.transition import SharedAxisTransition
from features.screenmanager import AppScreenManager
from ui.theme import ThemeManager

LabelBase.register(
    "Roboto",
    'assets/fonts/Poppins-Regular.ttf',
    'assets/fonts/Poppins-Italic.ttf',
    'assets/fonts/Poppins-Bold.ttf',
    'assets/fonts/Poppins-BoldItalic.ttf'
)
Loader.error_image = "assets/images/transparent.png"
Loader.loading_image = "assets/images/transparent.png"
register_factory()

if platform == "android":
    from kvdroid.tools.display import set_edge_to_edge

    set_edge_to_edge()


class MusicPlayerApp(App):
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
        self.sm = AppScreenManager(transition=SharedAxisTransition())
        box = BoxLayout()
        box.add_widget(self.sm)
        if platform == "android":
            self.sm.bind(
                current=lambda _, name: (
                    setattr(box, "padding", [0, self.statusbar_height, 0, self.navbar_height])
                    # if name != "home screen" else
                    # setattr(box, "padding", [0, 0, 0, self.navbar_height])
                )
            )
        self.sm.current = "player screen"
        return box

    def on_start(self):
        pass
        # win_md_bnb.create_bnb(
        #     tabs=[
        #         {
        #             "icon": "music-circle",
        #             "icon_variant": "music-circle-outline",
        #             "text": "Music",
        #             "name": "home screen",
        #             "active": True,
        #             "on_release": lambda _: setattr(self.sm, "current", "home screen"),
        #         },
        #         {
        #             "icon": "heart",
        #             "icon_variant": "heart-outline",
        #             "text": "Favorites",
        #             "name": "favorite screen",
        #             "on_release": lambda _: setattr(self.sm, "current", "favorite screen"),
        #         }
        #     ],
        #     use_text=False
        # )
        # win_md_bnb.push()


if __name__ == '__main__':
    import trio

    app = MusicPlayerApp()
    trio.run(app.async_run, "trio")
