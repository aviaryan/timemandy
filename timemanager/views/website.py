from timemanager import app
from flask import render_template


# home route
@app.route('/')
def home():
    return render_template('index.html')
