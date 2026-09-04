"""Consent-based local webcam broadcast demo.

Run this file, then open http://127.0.0.1:5000/ in a browser.
Frames are kept in memory only and are not written to disk.
"""

import os
import threading
from urllib.parse import urlparse

from flask import Flask, Response, abort, render_template, request

app = Flask(__name__)
frame_condition = threading.Condition()
latest_frame = None


def iframe_url():
    value = app.config.get("IFRAME_URL", os.environ.get("BROADCAST_IFRAME_URL", "https://example.com"))
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return "https://example.com"
    return value


@app.get("/")
def viewer():
    return render_template("cam.html", iframe_url=iframe_url())


@app.get("/cam")
def camera_source():
    return render_template("index.html")


@app.post("/frame")
def receive_frame():
    global latest_frame
    frame = request.get_data(cache=False, as_text=False)
    if not frame or len(frame) > 2_000_000 or not frame.startswith(b"\xff\xd8"):
        abort(400)
    with frame_condition:
        latest_frame = frame
        frame_condition.notify_all()
    return ("", 204)


def mjpeg_stream():
    while True:
        with frame_condition:
            frame_condition.wait_for(lambda: latest_frame is not None)
            frame = latest_frame
        yield b"--frame\r\nContent-Type: image/jpeg\r\nContent-Length: " + str(len(frame)).encode() + b"\r\n\r\n" + frame + b"\r\n"


@app.get("/stream.mjpg")
def stream():
    return Response(mjpeg_stream(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.get("/snapshot.jpg")
def snapshot():
    with frame_condition:
        if latest_frame is None:
            abort(404)
        frame = latest_frame
    return Response(frame, mimetype="image/jpeg")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, threaded=True)
