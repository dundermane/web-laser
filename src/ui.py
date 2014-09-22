

import os
import datetime
from flask import Flask, jsonify, render_template, request, redirect, url_for, Response
from werkzeug import secure_filename
import tempfile
import sender
import interpreter

ALLOWED_FILE = set(['dxf','jpeg','png','bmp','jpg'])

app = Flask(__name__, static_folder='web/static', static_url_path='')
app.template_folder = "web"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE, filename.rsplit('.', 1)[1]

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
    return Response(sender.send(job), mimetype='text/plaintext')
        
@app.route('/convert', methods=['POST'])
def convert():
    print 'converting'
    if request.method == 'POST':
        file = request.files['fileConvert']
        if file and allowed_file(file.filename):
            print file, allowed_file(file.filename)
            filetype = allowed_file(file.filename)[1]
            filename = secure_filename(file.filename)
            if filetype == 'dxf':
                try:
                    job = interpreter.Interpret(file.stream)
                except:
                    job = {'success':[False, 'There\'s something funky with you DXF']}
                job['success'] = [True, 'Successfully Converted DXF']
                return jsonify(job)
            if allowed_file(file.filename)[0]:
                job = {'success':[False, 'Fail. Currently unsupported filetype']}
                return jsonify(job)
            else:
                job = {}
                job['success'] = [False, 'Fail. Filetype not even close']
                return jsonify(job)
            

if __name__ == "__main__":
    app.run(host='::', port=80)

