from os.path import join, dirname, basename

from kivy.animation import Animation
from kivy.clock import triggered
from kivy.lang import Builder
from kivy.metrics import sp, dp
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout

from components.button import CustomButton
from features.basescreen import BaseScreen
from libs.image import extract_thumbnail_file_from_mp3
from libs.serialize import serialize

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class PlayerScreen(BaseScreen):
    """
    Manages the player screen, including music playback, UI updates, playlist management,
    and handling of user interactions. This class bridges the user interface and the player mechanics,
    allowing users to interact with and control media playback effectively.

    This class is responsible for managing player functionalities like play, pause, shuffle, repeat,
    and navigation between tracks. It handles UI transitions and updates to ensure dynamic behavior
    while the user interacts with the player. It also manages audio permissions and initializes
    the playlist from available audio files.

    :ivar player: Instance of the media player used for playback management.
    :type player: ExoPlayer
    :ivar permission_granted: Determines if audio-related permissions are granted to the application.
    :type permission_granted: bool
    """
    def __init__(self, **kwargs):
        """
        Represents the initialization of a class that sets up default properties for the instance. The
        constructor accepts any keyword arguments, but only specific attributes are directly initialized.
        By default, `player` is set to None, and `permission_granted` is initialized as False.

        :param kwargs: Additional keyword arguments for further configurations. These are not directly
                       utilized within this initializer.
        """
        super().__init__(**kwargs)
        self.player = None
        self.permission_granted = False

    def push_up(self):
        """
        Pushes up certain UI elements in an animated fashion to create a visual
        transition effect in the application. This method manages animations for a
        playlist container, background overlay, player container, and player preview,
        ensuring a cohesive user interface experience for displaying player-related
        content.

        :raises AttributeError: If certain widget IDs are not properly defined in the
                                 current class or if the height properties are missing.
        :raises TypeError: If invalid types are passed to any animation parameters by
                            mistake during execution.
        """
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
        """
        Adds an overlay button to the interface. This button is styled with a custom font
        and includes a message prompting the user to swipe down to hide. The button also
        registers an event to trigger the `push_down` function when pressed. It visually
        integrates with the existing overlay by being added as a child widget to the
        'overlay' context in the interface.

        :returns: None
        """
        self.ids.rv.disabled = True
        icon_path = "assets/fonts/materialdesignicons-webfont.ttf"
        button = CustomButton(
            size_hint_y=None,
            height=dp(80),
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
        """
        Handles the animation for elements within the application when the push_down
        method is invoked. This function transitions the UI elements such as the play
        list container, overlay, player container, and player preview to specific
        positions with animations, altering their visibility or opacity as required.

        :param self: Instance of the parent class containing UI element references and
            methods.
        :return: None
        """
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
        """
        Removes the overlay button widget from the overlay container.

        This method accesses the overlay container via its `ids` property. It then
        removes the first widget (typically the most recently added widget) from the
        list of children within the overlay container. This operation modifies the
        children list of the container by removing the targeted widget.

        :raises KeyError: If the `overlay` key is not found in `self.ids`.
        :raises IndexError: If the `children` list of `overlay` is empty.
        :return: None
        """
        overlay = self.ids.overlay
        overlay.remove_widget(overlay.children[0])

    def play(self, music_index=None):
        """
        Plays the currently loaded media or seeks to a specific media item index if
        provided. This function interacts with the player instance for media playback
        and updates the user interface to reflect the playback status.

        :param music_index: The index of the media item to play. If None, the current
            media playback is resumed or initiated.
        :type music_index: int | None
        :return: None
        """
        if music_index is None:
            if not self.player:
                return
            self.player.prepare()
            self.player.play()
        else:
            self.update_progress.cancel()
            self.player.seek_to_media_item_index(music_index)
            self.player.play()
            self.update_player_ui(self.ids.rv.data[music_index])

        self.update_progress()
        self.set_pause_button()

    def pause(self):
        """
        Pauses the media player, cancels the progress update,
        and updates the play button state.

        :return: None
        """
        self.player.pause()
        self.update_progress.cancel()
        self.set_play_button()

    def next(self):
        """
        Advances the player to the next item in the playlist, starts playback, updates
        the UI to reflect the current state, and reinitializes periodic updates for the
        progress bar.

        :return: None
        """
        self.update_progress.cancel()
        self.player.seek_to_next()
        self.player.play()
        self.set_pause_button()
        self.update_progress()

    def previous(self):
        """
        Navigates to the previous track in the playlist.

        This method cancels the current progress update task, skips to the
        previous track in the playlist, resumes playback, updates the interface
        to reflect the playback state, and restarts the progress update process.

        :return: None
        """
        self.update_progress.cancel()
        self.player.seek_to_previous()
        self.player.play()
        self.set_pause_button()
        self.update_progress()

    def shuffle(self):
        """
        Enables the shuffle mode for the player's playback.

        This method activates the shuffle functionality in the player, allowing
        it to play tracks, items, or media in a randomized order. This is typically
        used to enhance playback variety and prevent repetitive sequencing.

        :return: None
        """
        self.player.set_shuffle_mode_enabled(True)

    def repeat(self):
        """
        Sets the player's repeat mode.

        This function sets the playback repeat mode of the player to repeat all
        tracks. It modifies the player's internal state to enable continuous
        repeat for all tracks in the playlist.

        :raises AttributeError: If `self.player` or its methods/attributes are
            not properly defined.
        :return: None
        """
        self.player.set_repeat_mode(self.player.REPEAT_MODE_ALL)

    def set_pause_button(self):
        """
        Sets the "pause" icon for the preview and container play buttons.

        This method updates both the `preview_play_btn` and `container_play_btn`
        to display a "pause" icon, which is typically used to indicate that
        the current state has shifted to a paused state requiring user action
        to resume.

        :param self: Instance of the class where this method is called.
        :return: None
        """
        self.ids.preview_play_btn.icon = "pause"
        self.ids.container_play_btn.icon = "pause"

    def set_play_button(self):
        """
        Sets the icons for preview play button and container play button to "play".

        This method updates the respective UI elements' icon attribute, ensuring they
        both display the "play" icon.

        :return: None
        """
        self.ids.preview_play_btn.icon = "play"
        self.ids.container_play_btn.icon = "play"

    def request_audio_permission(self):
        """
        Requests audio-related permissions from the system and updates the playlist upon
        successful permission grant.

        This function leverages the Android permissions system to request the necessary
        permissions for accessing audio media and external storage. Upon successfully
        granting the required permissions, it sets the `permission_granted` attribute
        to True and invokes the `update_playlist` method.

        :param self: Instance of the class that invokes this method.

        :return: None
        """
        from android.permissions import request_permissions, Permission  # noqa

        def callback(_, results):
            if not any(results):
                return
            self.permission_granted = True
            self.update_playlist()

        request_permissions(
            [
                Permission.READ_MEDIA_AUDIO,
                Permission.READ_EXTERNAL_STORAGE
            ]
            , callback
        )

    def on_enter(self, *args):
        """
        Handles the logic for entering an event and requesting audio permissions if not already granted.

        :param args: Arbitrary positional arguments passed to the method.
        :return: None
        """
        if self.permission_granted:
            return
        self.request_audio_permission()

    @triggered(1)
    def update_playlist(self):
        """
        Updates the current playlist with available audio files and updates the corresponding
        UI elements to display the information of the first audio file in the playlist.

        The method initializes the ExoPlayer instance if it is not already initialized. It fetches
        all audio files, generates media items for playback, and thumbnails for display if not present.
        The playlist's UI elements are updated accordingly.

        :param self: The instance of the class that contains this method.
        :raises KeyError: If any expected dictionary keys (e.g., 'uri', 'title', 'artist', 'data')
            are missing from the audio file information.
        :raises ValueError: If there are issues processing media files or creating media items.
        :return: None
        """
        from kvdroid.tools.audio import get_all_audio_files
        from kvdroid.tools.appsource import app_dirs
        from kvdroid.tools.exoplayer import ExoPlayer

        if not self.player:
            self.player = ExoPlayer()

        media_items = []
        audio_files = get_all_audio_files()
        rv_data = []

        for i, music in enumerate(audio_files):
            if music["thumbnail"]:
                thumbnail_file = extract_thumbnail_file_from_mp3(music["data"], app_dirs("ext_cache"))
                music["thumbnail"] = thumbnail_file
            else:
                music["thumbnail"] = "assets/images/thumbnail.png"

            rv_data.append({
                "title": music["title"],
                "artist": music["artist"],
                "thumbnail": music["thumbnail"],
                "on_release": lambda music_index=i: self.play(music_index)
            })

            media_items.append(self.player.media_item_from_uri(music["uri"]))

        if not rv_data:
            self.ids.rv.data = []
            self.ids.preview_title.text = "No music found"
            self.ids.container_title.text = "No music found"
            self.ids.preview_artist.text = "Empty"
            self.ids.container_artist.text = "Empty"
            self.ids.preview_thumbnail.source = "assets/images/thumbnail.png"
            self.ids.container_thumbnail.source = "assets/images/thumbnail.png"
            return

        self.ids.rv.data = rv_data
        self.update_player_ui(rv_data[0])

        self.player.set_media_items(serialize(media_items))
        self.player.prepare()

    @triggered(1/24, True)
    def update_progress(self):
        """
        Updates the progress of the media playback and UI elements of the player. This method
        is designed to maintain synchronization between the media playback state and the
        corresponding UI components within the application. The progress is calculated as a
        ratio of the current playback position to the total duration of the media.

        This method is triggered periodically to ensure UI updates during media playback,
        and it stops automatically when media reaches a terminal state like `STATE_ENDED`
        or `STATE_IDLE`.

        :raises AnyRaisedError: The method documentation does not list explicitly raised
            errors.

        :return: No return value
        """
        player = self.player
        if player.is_command_available(player.COMMAND_GET_CURRENT_MEDIA_ITEM):
            self.update_player_ui(self.ids.rv.data[self.player.get_current_media_item_index()])
            current_position = player.get_current_position()
            duration = player.get_duration()
            if duration <= 0:
                return
            progress = current_position / duration
            self.ids.preview_progress.value = progress
            self.ids.container_progress.value = progress
            if self.player.get_playback_state() in [self.player.STATE_ENDED, self.player.STATE_IDLE]:
                self.update_progress.cancel()
                self.set_play_button()
                self.ids.preview_progress.value = 0
                self.ids.container_progress.value = 0

    def update_player_ui(self, music_data):
        """
        Updates the player user interface with the provided music data. This method modifies
        the text and image elements within the interface to display updated song information
        such as title, artist, thumbnail image, and initializes the progress bar to zero for both
        the preview and container sections.

        :param music_data: A dictionary containing the music details to be displayed. Keys include:
            - 'title': The title of the song.
            - 'artist': The name of the artist.
            - 'thumbnail': URL or file path to the song's thumbnail image.
        :type music_data: dict

        :return: None.
        """
        self.ids.preview_title.text = music_data["title"]
        self.ids.container_title.text = music_data["title"]

        self.ids.preview_artist.text = music_data["artist"]
        self.ids.container_artist.text = music_data["artist"]

        self.ids.preview_thumbnail.source = music_data["thumbnail"]
        self.ids.container_thumbnail.source = music_data["thumbnail"]

        self.ids.preview_progress.value = 0
        self.ids.container_progress.value = 0


class PlayList(ButtonBehavior, BoxLayout):
    """
    Represents a playlist item, combining various properties such as
    title, artist, and thumbnail information.

    This class inherits ButtonBehavior to provide interactivity and
    BoxLayout for layout design. It is used within the application to
    display and manage playlist items with associated metadata.

    :ivar title: The title of the playlist item.
    :type title: str
    :ivar artist: The artist associated with the playlist item.
    :type artist: str
    :ivar thumbnail: The URL or path to the thumbnail image for the
        playlist item.
    :type thumbnail: str
    """
    title = StringProperty()
    artist = StringProperty()
    thumbnail = StringProperty()
