import nltk
from flask import Flask, request, render_template, flash, redirect, session, abort, jsonify
from models import Model
from stress_detection_tweets import DepressionDetection
from TweetModel import process_message
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)








nltk.download('stopwords')

set(stopwords.words('english'))



# Home route
@app.route('/')
def root():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')

# Login route
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'admin' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return root()

# Logout route
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return root()

# File Upload
@app.route('/upload')
def upload():
    return render_template('upload.html')  

# Prediction Page
@app.route('/prediction1')
def prediction1():
    return render_template('index.html')  

# Chart Page
@app.route('/chart')
def chart():
    return render_template('chart.html') 

# File Preview Route
@app.route('/preview', methods=["POST"])
def preview():
    if request.method == 'POST':
        dataset = request.files['datasetfile']
        df = pd.read_csv(dataset, encoding='unicode_escape')
        df.set_index('Id', inplace=True)
        return render_template("preview.html", df_view=df) 

# Sentiment Analysis Page
@app.route("/sentiment")
def sentiment():
    return render_template("sentiment.html")

# Additional Pages
@app.route('/healthy_tips')
def healthy_tips():
    return render_template('healthy_tips.html')

@app.route('/screen_time')
def screen_time():
    return render_template('screen_time.html')

@app.route('/digital_detox')
def digital_detox():
    return render_template('digital_detox.html')

@app.route('/professional_help')
def professional_help():
    return render_template('professional_help.html')

@app.route('/rehabilitation')
def rehabilitation():
    return render_template('rehabilitation.html')

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    email = request.form["email"]
    subject = request.form["subject"]
    message = request.form["message"]

    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (name, email, subject, message) VALUES (?, ?, ?, ?)",
                   (name, email, subject, message))
    conn.commit()
    conn.close()

    
    return redirect("/thank-you")

# Thank You Page
@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html") # Redirect back to the homepage

# Sentiment Prediction Route
@app.route("/predictSentiment", methods=["POST"])
def predictSentiment():
    stop_words = stopwords.words('english')
    message = request.form.get('form10', '')  # Ensure 'message' is always defined
    text_final = ''.join(c for c in message if not c.isdigit())

    # Remove stopwords
    processed_doc1 = ' '.join([word for word in text_final.split() if word not in stop_words])

    sa = SentimentIntensityAnalyzer()
    dd = sa.polarity_scores(text=processed_doc1)
    compound = round((1 + dd['compound']) / 2, 2)

    return render_template("tweetresult.html", 
                           result=compound, 
                           text1=text_final, 
                           text2=dd['pos'], 
                           text5=dd['neg'], 
                           text4=compound, 
                           text3=dd['neu'],
                           message=message)  # Ensure message is passed

# Gadget Addiction Prediction Route
@app.route('/predict', methods=["POST"])
def predict():
    q1 = int(request.form['a1'])
    q2 = int(request.form['a2'])
    q3 = int(request.form['a3'])
    q4 = int(request.form['a4'])
    q5 = int(request.form['a5'])
    q6 = int(request.form['a6'])
    q7 = int(request.form['a7'])
    q8 = int(request.form['a8'])
    q9 = int(request.form['a9'])
    q10 = int(request.form['a10'])

    values = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
    model = Model()
    classifier = model.svm_classifier()
    prediction = classifier.predict([values])

    if prediction[0] == 0:
        result = 'Your Gadget Addiction test result: Stage 1: No Impact of Addiction.'
    elif prediction[0] == 1:
        result = 'Your Gadget Addiction test result: Stage 2: Moderate Usage with Minor Impact'
    elif prediction[0] == 2:
        result = 'Your Gadget Addiction test result: Stage 3: Frequent Usage with Noticeable Impact'
    elif prediction[0] == 3:
        result = 'Your Gadget Addiction test result: Stage 4: High Usage with Significant Impact'
    else:
        result = 'Your Gadget Addiction test result: Stage 5: Severe Dependency with Major Impact'

    return render_template("result.html", result=result, message="Gadget Addiction Test")  # Ensure message is passed

# Secret Key and Running the App
app.secret_key = os.urandom(12)
app.run(port=5987, host='0.0.0.0', debug=True) 