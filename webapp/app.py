""" This is the main application file. """
from flask import Flask, abort, flash, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap

import auth
import os
import relay

APP = Flask(__name__)
APP.config.from_pyfile("config.py")
bootstrap = Bootstrap(APP)

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
            flash(action + " button pressed")
            return redirect(url_for('index'))
        else:
            abort(500)
    else:
        abort(403)

@APP.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@APP.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    relay.init()
    APP.run(debug=True, host="0.0.0.0")
    relay.cleanup()
