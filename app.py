from flask import Flask, request, Response
import json, time, threading, urllib2, re
import flask
import json
import socket
import os
import commands

app = Flask(__name__)
app.debug = True

masters = {}
clients = {}
idle_checking = False
master_scanning = False
ip_root = 'http://10.0.0.'
port = '1337'

found_wlan = False
found_en = False
lanIp = ''
for line in commands.getoutput("ifconfig").split("\n"):
    if found_wlan or found_en:
        if found_wlan:
            matches = re.search(r'inet addr:(\S+)', line)
        else:
            matches = re.search(r'inet (\S+)', line)
        if matches:
            lanIp = matches.group(1)
    elif re.match(r'wlan', line):
        found_wlan = True
    elif re.match(r'en0', line):
        found_en = True


print "testtt" + lanIp

@app.route('/state')
def connect():
    global clients, idle_checking, master_scanning

    if request.remote_addr in clients:
        clients[request.remote_addr]['timestamp'] = time.time()
    else:
        clients[request.remote_addr] = {
            'timestamp': time.time(),
            'stream': '',
            'volume': 50,
            'owner': -1
        }
    
    if not idle_checking:
        thread = threading.Thread(target=disconnect_idles)
        thread.start()

        idle_checking = True

    if not master_scanning:
        thread = threading.Thread(target=master_scan)
        thread.start()

        master_scanning = True

    return Response(json.dumps(clients[request.remote_addr]),  mimetype='application/json')

@app.route('/clients')
def get_clients():
    return Response(json.dumps(clients),  mimetype='application/json')

@app.route('/changeOwner', methods=['POST'])
def change_owner():
    global clients
    req = request.form

    remote = req['name']
    clients[remote]['owner'] = int(req['owner'])
    clients[remote]['stream'] = 'http://10.0.0.5:3251/stream'
    if clients[remote]['owner'] == -1:
        clients[remote]['stream'] = ''
    print clients
    return ''

@app.route('/')
def index():
    listActive = []
    listAvailable = []
    for client in clients:
        if clients[client]['owner'] == -1:
            listAvailable.append({'name': client})
        else:
            listActive.append({'name': client})

    return flask.render_template('index.html', listActive=listActive, listAvailable=listAvailable, device={"name": lanIp, "ip": lanIp})

def disconnect_idles():
    while len(clients) > 0:
        clients_to_pop = []
        for client in clients:
            if (time.time() - clients[client]['timestamp'] > 30):
                clients_to_pop.append(client)
        for client in clients_to_pop:
            print 'AFTER'
            clients.pop(client)
        time.sleep(10)
    idle_checking = False

def master_scan():
    while True:
        new_masters = []
        for i in range(10):
            try:
                content = urllib2.urlopen(ip_root + str(i) + ":" + str(port) + "/state").read()
                new_masters.append(i)
            except:
                pass
        masters = new_masters
        time.sleep(10)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1337)
