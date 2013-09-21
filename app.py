from flask import Flask
import json

app = Flask(__name__)

clients = []

@app.route('/connect')
def connect():
    return True

@app.route('/')
def app():
    return False

if __name__ == '__main__':
    app.run(hostname="127.0.0.1", port=80085)
