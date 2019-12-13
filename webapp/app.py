"This is the web application that operates the relays."

from flask import Flask, render_template, redirect, request, abort
from flask_bootstrap import Bootstrap

import relay

app = Flask(__name__)
Bootstrap(app)

LEFT = 0
RIGHT = 1
RELAYS = {'Left':LEFT, 'Right':RIGHT}

@app.route('/', methods = ['POST', 'GET'])
def index():
    "This is the main (only) path for operating both relays."

    if request.method == 'GET':
        return render_template("index.html")

    if request.method == 'POST':
        action = request.form['action']
        if action in RELAYS.keys():
            relay.press(RELAYS[action])
            return redirect("/")
        else:
            abort(400)

if __name__ == '__main__':
    relay.init()
    app.run(debug=True, host='0.0.0.0')
    relay.cleanup()
