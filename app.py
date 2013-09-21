from flask import Flask
import json

app = Flask(__name__)
app.debug = True

clients = []

@app.route('/connect')
def connect():
    return "hello World"

@app.route('/')
def helo():
    return "hello world"

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=1337)
