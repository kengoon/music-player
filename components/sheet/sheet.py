__all__ = ("BaseSheet", "OtpSheet",)

from kivy.animation import Animation
from kivy.clock import mainthread
from kivy.metrics import dp
from kivy.properties import VariableListProperty, NumericProperty, StringProperty, BooleanProperty, ObjectProperty
from kivy.clock import ClockEvent, Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from os.path import join, dirname, basename
from kivy.core.window import Window
from kivy.uix.modalview import ModalView

from components.behaviors import AdaptiveBehavior
from kivy import platform

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))

clock: ClockEvent = None


class BaseSheet(ButtonBehavior, BoxLayout):
    __events__ = ("on_open", "on_dismiss")
    is_open = BooleanProperty(False)
    screen = ObjectProperty()
    radius = VariableListProperty(["20dp", "20dp", 0, 0])
    bottom_padding = NumericProperty("20dp")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.modalview = ModalView(
            background_color=(0, 0, 0, 0),
            background="",
            overlay_color=(0, 0, 0, .4),
            auto_dismiss=False,
        )
        if platform == "android":
            from kvdroid.tools.display import get_navbar_height
            self.bottom_padding = self.bottom_padding + get_navbar_height()

    def open(self):
        if self.is_open:
            return
        for child in Window.children:
            if child.__class__ == self.__class__:
                del self
                return
        self.modalview.open(animate=True)
        Window.add_widget(self)
        self._open()

    def _open(self):
        anim = Animation(y=0, duration=.2)
        anim.bind(on_complete=lambda *_: self.dispatch("on_open"))
        anim.start(self)
        self.is_open = True

    def dismiss(self):
        if not self.is_open:
            return
        anim = Animation(y=-self.height - dp(50), duration=.2)
        anim.bind(on_complete=self._dismiss)
        anim.start(self)
        self.is_open = False

    def _dismiss(self, *_):
        Window.remove_widget(self)
        self.modalview.dismiss()
        self.dispatch("on_dismiss")

    def on_open(self, *args):
        pass

    def on_dismiss(self, *args):
        pass


class OtpSheet(BaseSheet, AdaptiveBehavior):
    __events__ = ("on_submit_otp", "on_resend_otp")
    timeout = NumericProperty(60)
    phone_number = StringProperty("08136346373")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global clock
        self._countdown_callback = lambda _: setattr(self, "timeout", self.timeout - 1)
        clock = Clock.create_trigger(
            self._countdown_callback,
            timeout=1,
            interval=True
        )
        self.bind(timeout=lambda _, tmo: clock.cancel() if tmo == 0 else None)

    def _open(self):
        anim = Animation(y=0, duration=.2)
        anim.bind(on_complete=lambda *_: clock())
        anim.start(self)
        self.is_open = True
        self.dispatch("on_open", self)

    def _dismiss(self, *_):
        super()._dismiss(*_)
        clock.cancel()

    def submit_otp(self):
        if self.ids.spinner.active:
            return
        self.ids.spinner.active = True
        otp = self.ids.otp.text
        self.dispatch("on_submit_otp", otp)

    def resend_otp(self):
        self.dispatch("on_resend_otp")
        self.timeout = self.property("timeout").defaultvalue
        clock()

    def stop_spinner(self):
        self.ids.spinner.active = False

    def on_submit_otp(self, otp):
        pass

    def on_resend_otp(self):
        pass

