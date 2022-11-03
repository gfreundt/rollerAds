"""This Code Runs on Each Player"""

import threading
import json
import vlc
import time
import os
import platform
import filetype
import cv2
from datetime import datetime as dt
from datetime import timedelta as td
from flask import Flask, render_template, redirect, request, url_for


class Startup:
    def __init__(self):
        self.player = vlc.MediaPlayer()
        self.player.set_fullscreen(True)
        directories = {
            "Windows": r"C:\pythonCode\rollerAds\player\media",
            "Linux": r"/home/pi/pythonCode/rollerAds/player/media",
        }
        self.media_directory = directories[platform.system()]
        self.form_defaults = {
            "name": "nametest",
            "duration": 10,
            "start_date": "2021-10-25",
            "start_time": "18:04",
            "end_date": "2022-10-26",
            "end_time": "22:34",
        }
        self.app = Flask(__name__)

    def load_storyboard(self):
        """Load JSON file that gives player the media information to play on a loop"""

        with open("storyboard_active.json", mode="r") as json_file:
            storyboard = json.load(json_file)
            media = storyboard["media"]

        active = [i for i in media.values() if i["active"] and i["aka_name"]]
        inactive = [i for i in media.values() if not i["active"] and i["aka_name"]]
        loaded_media = [i["file_name"] for i in media.values()]
        unloaded_media = [
            i
            for i in os.listdir(os.path.join(os.getcwd(), "media"))
            if i not in loaded_media
        ]
        return {"active": active, "inactive": inactive, "unloaded": unloaded_media}


def form_defaults(filename):
    print(filename)

    cap = cv2.VideoCapture(filename)
    fps = cap.get(cv2.CAP_PROP_FPS)  # OpenCV v2.x used "CV_CAP_PROP_FPS"
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    d = int(frame_count * 10 / fps) / 10

    print(d)

    return {
        "name": filename.split(".")[1],
        "duration": d,
        "start_date": dt.strftime(dt.now(), "%Y-%m-%d"),
        "start_time": dt.strftime(dt.now(), "%H:%M"),
        "end_date": dt.strftime(dt.now() + td(days=1), "%Y-%m-%d"),
        "end_time": dt.strftime(dt.now(), "%H:%M"),
    }


def updater():
    def edit_position_properties(position):
        pass

    def active_to_inactive(position):
        pass

    def inactive_to_active(position):
        pass

    def delete_position(position):
        pass

    @PLAYER.app.route("/")
    @PLAYER.app.route("/loaded")
    def loaded():
        return render_template("loaded.html", data=PLAYER.load_storyboard())

    @PLAYER.app.route("/unloaded")
    def unloaded():
        return render_template("unloaded.html", data=PLAYER.load_storyboard())

    @PLAYER.app.route("/unsupported")
    def unsupported():
        return render_template("unsupported.html", data=PLAYER.load_storyboard())

    @PLAYER.app.route("/properties", methods=["POST", "GET"])
    def properties():
        if request.method == "POST":
            form_data = []
            for d in [
                "name",
                "duration",
                "start_date",
                "start_time",
                "end_date",
                "end_time",
            ]:
                form_data.append(request.form[d])
            print(form_data)
            return redirect(url_for("loaded"))
        else:
            filename = os.path.join(PLAYER.media_directory, "xyz.jpg")
            return render_template(
                "properties.html",
                data=PLAYER.load_storyboard(),
                defaults=form_defaults(filename),
                media=filename.split("\\")[-1],
            )

    PLAYER.app.run(host="0.0.0.0", debug=True)
    print("Updater Running")


def media_loop():
    """Thread that loops through all active media items and resets storyboard with each cycle"""
    t = time.perf_counter()
    while True:
        # reload storyboard with every cycle in case it has been changed by updater
        PLAYER.storyboard_active, _ = PLAYER.load_storyboard()
        # loop through all active media
        for to_be_played in PLAYER.storyboard_active:
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

    """
    updater_thread = threading.Thread(target=updater)
    media_loop_thread = threading.Thread(target=media_loop)

    updater_thread.start()
    media_loop_thread.start()
    """

    updater()


main()
