# This package is for additional application modules.
from kivy.clock import Clock
from kivy.core.text import Label
from kivy.metrics import sp

from libs.decorator import android_only


def shorten_text(text, lbl_width, lines=1, suffix="... See more", font_size=sp(12)):
    """
    Used to shorten text in kivy to number of lines you want unlike kivy which only shortens for
    one line

    :param text: text to shorten
    :param lbl_width: width of the original label containing the text to shorten
    :param lines: number of lines to shorten to
    :param suffix: suffix to add at the end of the text (e.g "suffix=.... see more")
    :param font_size: font_size of the original label containing the text to shorten
    :return: returns shorten text
    """
    lbl = Label(font_size=font_size)
    new_text = text
    text_width = lbl.get_cached_extents()
    t = 0
    lbl_width *= lines
    if lbl_width <= 0:
        return ""
    while text_width(new_text + suffix)[0] > lbl_width:
        new_text = new_text.split(" ")
        del new_text[-1]
        new_text = " ".join(new_text)
        if text_width(new_text + suffix)[0] == t:
            return ""
        t = text_width(new_text + suffix)[0]
    return new_text + suffix


def compute_text_size(text, font_size, padding, widget_width):
    if len(padding) < 4 or not isinstance(padding, list):
        raise TypeError("padding must be a list and of length 4")
    lbl = Label(text=text, font_size=font_size, padding=padding)
    lbl.refresh()
    height, width = lbl.size
    if width > (widget_width - (padding[0] + padding[2])):
        height_pad = padding[1] + padding[2]
        height = height - height_pad
        height *= (widget_width // width)
        height += height_pad
        return widget_width, height
    return width, height


def get_dict_pos(lst, key, value):
    return next((index for (index, d) in enumerate(lst) if d[key] == value), None)


def search_dict(search_term, data_key, data, case_sensitive=False):
    if case_sensitive:
        a = filter(lambda search_found: search_term in search_found[data_key], data)
    else:
        a = filter(lambda search_found: search_term.lower() in search_found[data_key].lower(), data)
    return list(a)


@android_only
def push_up_textinput(widget, scrollview=None, child=None, default_pad=None, focus=False):
    if default_pad is None:
        default_pad = [0, 0, 0, 0]
    from kvdroid.tools import check_keyboad_visibility_and_get_height
    _, height = check_keyboad_visibility_and_get_height()
    widget.padding = [*default_pad[:3], height + (default_pad[-1] / 2)] if focus else default_pad
    if child and scrollview and focus:
        Clock.schedule_once(lambda _: scrollview.scroll_to(child))
