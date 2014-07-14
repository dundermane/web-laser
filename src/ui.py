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

@app.route('/sendGcode',methods=['POST'])
def send_g():
    job = {}
    
    job['gcode'] = request.form['gcode']
    job['unit'] = request.form['unit']
    job['repeat'] = request.form['repeat']
	
    response = sender.send(job)
    return render_template('landing.html', response=response)
        

if __name__ == "__main__":
    app.run(host='::', port=1024)

