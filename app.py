from flask import Flask
import json

app = Flask(__name__)

clients = []

@app.route('/connect')
def connect():
    return True

if __name__ == '__main__':
    app.run()
