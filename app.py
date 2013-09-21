from flask import Flask
import flask
import json
import socket
import os
import commands

app = Flask(__name__)
app.debug = True

clients = []
listActive = [{"name": "Hello"}, {"name":"shit"}]
listAvailable = [{"name": "YOLO"}, {"name":"SHIT"}]
lanIp = ""

@app.before_request
def before_request():
    set_lan_ip()

@app.route('/connect')
def connect():
    return "hello World"

@app.route('/')
def index():
    return flask.render_template('index.html', listActive=listActive, listAvailable=listAvailable)

def set_lan_ip():
    lanIp = commands.getoutput("/sbin/ifconfig").split("\n")[10].split(" ")[1]

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=1337)
