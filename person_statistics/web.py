from flask import Flask, render_template, request

app = Flask(__name__)

@app.get('/')
def index():
    return render_template("how_to_use.html")
