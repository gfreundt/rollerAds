"""This Code Runs on Each Player"""

import threading
import json
import vlc
import time
import os
import platform


class Startup:
    def __init__(self):
        self.player = vlc.MediaPlayer()
        self.player.set_fullscreen(True)
        directories = {
            "Windows": r"C:\pythonCode\rollerAds\player\media",
            "Linux": r"\home/pi/pythonCode/rollerAds/player/media",
        }
        self.media_directory = directories[platform.system()]

    def load_storyboard(self):
        """Load JSON file that gives player the media information to play on a loop"""

        with open("storyboard_active.json", mode="r") as json_file:
            storyboard = json.load(json_file)
            media = storyboard["media"]

        queued = [i for i in media.values() if i["queued"] and i["aka_name"]]
        unqueued = [i for i in media.values() if not i["queued"] and i["aka_name"]]
        return queued, unqueued


def updater():
    print("Updater Running")


def media_loop():
    """Thread that loops thorugh all queued media items and resets stroyboard with each cycle"""
    t = time.perf_counter()
    while True:
        # reload storyboard with every cycle in case it has been changed by updater
        PLAYER.storyboard_queued, _ = PLAYER.load_storyboard()
        # loop through all queued media
        for to_be_played in PLAYER.storyboard_queued:
            media = vlc.Media(
                os.path.join(PLAYER.media_directory, to_be_played["file_name"])
            )
            PLAYER.player.set_media(media)
            PLAYER.player.play()
            time.sleep(to_be_played["cycle_duration"])
        # max time control (debuggin only)
        if time.perf_counter() - t > 20:
            return


def main():
    """Defines variables and launches both threads"""
    global PLAYER
    PLAYER = Startup()

    updater_thread = threading.Thread(target=updater)
    media_loop_thread = threading.Thread(target=media_loop)

    updater_thread.start()
    media_loop_thread.start()


main()
