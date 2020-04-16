""" This is the main application file. """
from flask import Flask, render_template, redirect, request, abort
from flask_bootstrap import Bootstrap

import auth
import os
import relay

APP = Flask(__name__)
APP.config.from_pyfile("config.py")
Bootstrap(APP)

LEFT = 0
RIGHT = 1
RELAYS = {"Left": LEFT, "Right": RIGHT}
MAC_LIST = APP.config['MAC_LIST']

@APP.route("/", methods=["POST", "GET"])
def index():
    """ This processes the default route. """
    if request.method == "GET":
        return render_template("index.html")

    if (request.method == "POST") and (auth.check(request.remote_addr, MAC_LIST)):
        action = request.form["action"]
        if action in RELAYS.keys():
            relay.press(RELAYS[action])
            return redirect("/")
        else:
            abort(400)
    else:
        abort(403)


if __name__ == "__main__":
    relay.init()
    APP.run(debug=True, host="0.0.0.0")
    relay.cleanup()
