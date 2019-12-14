from flask import Flask, render_template, redirect, request, abort
from flask_bootstrap import Bootstrap

import relay

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
Bootstrap(app)

LEFT = 0
RIGHT = 1
relays = { 'Left':LEFT, 'Right':RIGHT }

@app.route('/', methods = ['POST', 'GET'])
def index():

    if request.method == 'GET':
        return render_template("index.html")

    if request.method == 'POST':
        action = request.form['action']
        if action in relays.keys():
            relay.press(relays[action])
            return redirect("/")
        else:
            abort(400)

@app.after_request
def add_header(response):
    # response.cache_contro.no_store = True
    response.headers['Cache-Control'] = ("no-store, no-cache, "
                       "must-revalidate, post-check=0, pre-check=0, "
                       "max-age=0")
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    relay.init()
    app.run(debug=True, host='0.0.0.0')
    relay.cleanup()
