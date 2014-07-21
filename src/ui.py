##TODO:
#
#

import os
import datetime
from flask import Flask, jsonify, render_template, request, redirect, url_for
import sender

app = Flask(__name__, static_folder='web/static', static_url_path='')
app.template_folder = "web"
TEMPFOLDER = "tmp/"

ADMINIDENT = None

##START MAIN PAGE

@app.route("/")
def landing():
    now = datetime.datetime.now()
    return render_template('landing.html')

@app.route('/g',methods=['POST'])
def send_g():
    job = {}
    job['gcode'] = request.form['gcode']
    job['unit'] = request.form['unit']
    job['repeat'] = request.form['repeat']
    return sender.send(job)
        

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1024)

