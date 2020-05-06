""" This is the main application file. """
import logging
from logging.handlers import TimedRotatingFileHandler

import yaml

from flask import Flask, abort, flash, redirect, render_template
from flask import request, url_for
from flask_bootstrap import Bootstrap

import auth
import relay

HANDLER = TimedRotatingFileHandler("log/garage_opener.log",
                                   when="midnight", interval=1, backupCount=7)
logging.getLogger('werkzeug').addHandler(HANDLER)
APP = Flask(__name__)
APP.logger.setLevel(logging.INFO)
APP.logger.addHandler(HANDLER)

Bootstrap(APP)

with open('static/config.yaml', 'r') as yaml_file:
    try:
        data = yaml.load(yaml_file, Loader=yaml.FullLoader)
        
    except yaml.YAMLError as exception:
        APP.logger.error('Could not open YAML configuration file.')
        exit()

SEND_FILE_MAX_AGE_DEFAULT = data['SEND_FILE_MAX_AGE_DEFAULT']
MAC_LIST = data['MAC_LIST']
RELAYS = data['RELAYS']
RANGE = data['RANGE']
APP.secret_key = data['SECRET_KEY']

@APP.route("/", methods=["POST", "GET"])
def index():
    """ This processes the default route. """
    if request.method == "GET":
        return render_template("index.html")

    if (request.method == "POST") and \
            (auth.check(RANGE, request.remote_addr, MAC_LIST, APP.logger)):
        action = request.form["action"]
        if action in RELAYS.keys():
            relay.press(RELAYS[action], APP.logger)
            flash(f"{action} button pressed")
            APP.logger.warning(f'{action} button pressed by {auth.get_mac(request.remote_addr)}')
            return redirect(url_for('index'))
        else:
            APP.logger.error('Action other than Left or Right')
            abort(500)
    else:
        APP.logger.warning('POST attempted by %s', request.remote_addr)
        abort(403)


@APP.errorhandler(403)
def forbidden():
    " When an forbidden access occurs render the custom error page. "
    return render_template('403.html'), 403


@APP.errorhandler(500)
def internal_server_error():
    " When an internal server error occurs render the custom error page. "
    return render_template('500.html'), 500


if __name__ == "__main__":
    relay.init()
    APP.run(debug=False, host="0.0.0.0")
    relay.cleanup()
