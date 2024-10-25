

"""
        To Run this code: 
            # .\myenv\Scripts\activate
            # python app.py
"""

import glob
import os
import warnings
import textract
import requests
from flask import (Flask,session, g, json, Blueprint,flash, jsonify, redirect, render_template, request,
                   url_for, send_from_directory)
from gensim.summarization import summarize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
#from werkzeug import secure_filename
from werkzeug.utils import secure_filename


import pdf2txt as pdf
import PyPDF2

import screen
import search
import hashlib

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

app = Flask(__name__)

app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    USERNAME='admin',
    PASSWORD='admin',
    SECRET_KEY='development key',
    ALLOWED_EXTENSIONS={'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
))


app.config['UPLOAD_FOLDER'] = 'Original_Resumes/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

class jd:
    def __init__(self, name):
        self.name = name

def getfilepath(loc):
    temp = str(loc).split('\\')
    return temp[-1]
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif app.config['PASSWORD'] != request.form['password']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))


@app.route('/')
def home():
    x = []
    for file in glob.glob("./Job_Description/*.txt"):
        res = jd(file)
        x.append(jd(getfilepath(file)))
    print(x)
    return render_template('index.html', results = x)




@app.route('/results', methods=['GET', 'POST'])
def res():
    if request.method == 'POST':
        jobfile = request.form['des']
        print(jobfile)
        flask_return = screen.res(jobfile)
        
        print(flask_return)
        return render_template('result.html', results = flask_return)



@app.route('/resultscreen' ,  methods = ['POST', 'GET'])
def resultscreen():
    if request.method == 'POST':
        jobfile = request.form.get('Name')
        print(jobfile)
        flask_return = screen.res(jobfile)
        return render_template('result.html', results = flask_return)



@app.route('/resultsearch' ,methods = ['POST', 'GET'])
def resultsearch():
    if request.method == 'POST':
        search_st = request.form.get('Name')
        print(search_st)
    result = search.res(search_st)
    # return result
    return render_template('result.html', results = result)


@app.route('/Original_Resume/<path:filename>')
def custom_static(filename):
    return send_from_directory('./Original_Resumes', filename)

@app.route('/upload', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file part in the request")
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash("No file selected for uploading")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("Resume uploaded successfully")
            return redirect(url_for('home'))
        else:
            flash("File extension not allowed")
            return redirect(request.url)
    
    return render_template('upload.html')

if __name__ == '__main__':
   # app.run(debug = True) 
    app.run('127.0.0.1' , 5000 , debug=True)
    #app.run('0.0.0.0' , 5000 , debug=True , threaded=True)
    
