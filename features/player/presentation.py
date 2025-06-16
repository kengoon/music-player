from os.path import join, dirname, basename

from kivy.animation import Animation
from kivy.lang import Builder
from kivy.metrics import sp, dp
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout

from components.button import CustomButton
from features.basescreen import BaseScreen

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class PlayerScreen(BaseScreen):
    def push_up(self):
        anim = Animation(y=self.ids.play_list_container.height, d=.2)
        anim.start(self.ids.play_list_container)

        anim = Animation(bg_color=[1, 1, 1, 1], d=.2)
        anim.bind(on_complete=lambda *_: self._add_overlay_button())
        anim.start(self.ids.overlay)

        player_container = self.ids.player_container
        player_container_y = (self.height - player_container.height - ((self.height - player_container.height) / 1.5))
        player_container_y += + self.app.navbar_height
        anim = Animation(y=player_container_y, opacity=1, d=.2)
        anim.start(player_container)

        player_preview = self.ids.player_preview
        player_preview_y = -player_preview.height - self.app.navbar_height
        anim = Animation(y=player_preview_y, opacity=0, d=.2)
        anim.start(player_preview)

    def _add_overlay_button(self):
        self.ids.rv.disabled = True
        icon_path = "assets/fonts/materialdesignicons-webfont.ttf"
        button = CustomButton(
            size_hint_y=None,
            height=dp(100),
            markup=True,
            font_size="13sp",
            text=f"[font={icon_path}][size={int(sp(18))}]\U000F0045[/size][/font] swipe down to hide",
            on_press=lambda *_: self.push_down(),
        )
        button.bg_color = [0, 0, 0, 0]
        button.color = self.app.theme_cls.text_color[:3] + [0.7]
        overlay = self.ids.overlay
        overlay.add_widget(button)

    def push_down(self):
        plc = self.ids.play_list_container
        anim = Animation(y=self.height - plc.height, d=.2)
        anim.start(plc)

        anim = Animation(bg_color=[0, 0, 0, 0], d=.2)
        anim.bind(on_complete=lambda *_: self._remove_overlay_button())
        anim.start(self.ids.overlay)

        player_container = self.ids.player_container
        player_container_y = -player_container.height + dp(100)
        anim = Animation(y=player_container_y, opacity=0, d=.2)
        anim.start(player_container)

        player_preview = self.ids.player_preview
        player_preview_y = 0
        anim = Animation(y=player_preview_y, opacity=1, d=.2)
        anim.start(player_preview)

        self.ids.rv.disabled = False

    def _remove_overlay_button(self):
        overlay = self.ids.overlay
        overlay.remove_widget(overlay.children[0])


class PlayList(ButtonBehavior, BoxLayout):
    title = StringProperty()
    artist = StringProperty()

    def on_release(self):
        print("yeas")
