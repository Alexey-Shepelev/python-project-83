from flask import Flask, render_template
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()


@app.route('/')
def index():
    return render_template('index.html')
