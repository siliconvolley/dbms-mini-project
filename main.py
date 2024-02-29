from flask import Flask

app = Flask(__name__)

@app.route("/")
def welcome_page():
    return "<p>Welcome to Company Energy Monitoring System</p>"