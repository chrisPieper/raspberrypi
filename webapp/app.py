""" This is the main application file. """
from flask import Flask, abort, flash, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap
from flask.logging import default_handler

import auth
import logging
import os
import relay
import time

from logging.handlers import TimedRotatingFileHandler

handler = TimedRotatingFileHandler("log/garage_opener.log",
                                    when="midnight",
                                    interval=1,
                                    backupCount=7)
logging.getLogger('werkzeug').addHandler(handler)
APP = Flask(__name__)
APP.logger.setLevel(logging.INFO)
APP.logger.addHandler(handler)

bootstrap = Bootstrap(APP)
APP.config.from_pyfile("config.py")

LEFT = 0
RIGHT = 1
RELAYS = {"Left": LEFT, "Right": RIGHT}
MAC_LIST = APP.config['MAC_LIST']

@APP.route("/", methods=["POST", "GET"])
def index():
    """ This processes the default route. """
    if request.method == "GET":
        return render_template("index.html")

    if (request.method == "POST") and (auth.check(request.remote_addr, MAC_LIST, APP.logger)):
        action = request.form["action"]
        if action in RELAYS.keys():
            relay.press(RELAYS[action])
            flash(action + " button pressed")
            APP.logger.warning('%s button pressed by %s', 
                action, 
                auth.get_mac(request.remote_addr))
            return redirect(url_for('index'))
        else:
            APP.logger.error('Action other than Left or Right')
            abort(500)
    else:
        APP.logger.warning('POST attempted by %s', request.remote_addr)
        abort(403)

@APP.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@APP.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    relay.init()
    APP.run(debug=False, host="0.0.0.0")
    relay.cleanup()
