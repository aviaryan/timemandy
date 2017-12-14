from timemanager import app
from flask import render_template


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
