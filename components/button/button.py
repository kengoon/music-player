__all__ = ('IconButton', 'CustomButton')

from kivy.properties import ColorProperty, ListProperty, VariableListProperty
from kivy.uix.behaviors import TouchRippleButtonBehavior
from kivy.lang import Builder
from os.path import join, dirname, basename

from kivy.uix.widget import Widget

from components.behaviors import StencilBehavior
from components.label import Icon, CustomLabel

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class IconButton(TouchRippleButtonBehavior, Icon):
    pass


class CustomButton(TouchRippleButtonBehavior, CustomLabel):
    text_size = ListProperty([None, None])
