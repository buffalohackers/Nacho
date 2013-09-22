from flask import Flask, request, Response
import json, time, threading, urllib2, re
import flask
import json
import socket
import os
import commands

app = Flask(__name__)
app.debug = True

clients = {}
idle_checking = False
master_scanning = False
ip_root = '10.0.0.'
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

lock = threading.Lock()

@app.route('/state')
def connect():
    global clients, idle_checking, master_scanning, lock

    with lock:
        if request.remote_addr in clients:
            clients[request.remote_addr]['timestamp'] = time.time()
        else:
            clients[request.remote_addr] = {
                'ip': request.remote_addr,
                'timestamp': time.time(),
                'stream': '',
                'volume': 50,
                'master': False,
                'owner': -1
            }
    
    if not idle_checking:
        thread = threading.Thread(target=disconnect_idles)
        thread.daemon = True
        thread.start()

        idle_checking = True

    
    return Response(json.dumps(clients[request.remote_addr]),  mimetype='application/json')

@app.route('/clients')
def get_clients():
    return Response(json.dumps(clients),  mimetype='application/json')

@app.route('/changeOwner', methods=['POST'])
def change_owner():
    global clients, lock
    req = request.form

    remote = req['name']
    with lock:
        clients[remote]['owner'] = int(req['owner'])
        clients[remote]['stream'] = 'http://' + lanIp + ':3251/stream'
        if clients[remote]['owner'] == -1:
            clients[remote]['stream'] = ''
    return ''

@app.route('/')
def index():
    global lock
    listActive = []
    listAvailable = []
    print "here"
    with lock:
        for client in clients:
            if not clients[client]['master']:
                if clients[client]['owner'] == -1:
                    listAvailable.append({'name': client})
                else:
                    listActive.append({'name': client})
    print "almost"
    return flask.render_template('index.html', listActive=listActive, listAvailable=listAvailable, device={"name": lanIp, "ip": lanIp})

@app.route('/updateVolume', methods=['POST'])
def update_volume():
    global clients, lock
    req = request.form

    remote = req['name']
    with lock:
        clients[remote]['volume'] = req['volume']

    return ''

@app.route('/getMasters')
def get_masters():
    global lock
    masters = []
    with lock:
        for client in clients:
            if clients[client]['master']:
                masters.append(clients[client])

    return Response(json.dumps(masters),  mimetype='application/json')

@app.route('/listStreams')
def list_streams():
	global lock
	masters = []
	with lock:
		for client in clients:
			if clients[client]['master']:
				masters.append(clients[client])

	return flask.render_template("streams.html", masters=masters)

@app.route('/getSpeakers')
def get_speakers():
    global lock
    speakers = []
    with lock:
        for client in clients:
            if not clients[client]['master']:
                speakers.append(clients[client])

    return Response(json.dumps(speakers),  mimetype='application/json')

def disconnect_idles():
    global lock
    while len(clients) > 0:
        clients_to_pop = []
        with lock:
            for client in clients:
                if (time.time() - clients[client]['timestamp'] > 30):
                    clients_to_pop.append(client)
            for client in clients_to_pop:
                clients.pop(client)
        time.sleep(10)
    idle_checking = False

def master_scan():
    global clients
    while True:
        for i in range(10):
            thread = threading.Thread(target=ping_state, args=(i,))
            thread.start()

        time.sleep(10)
        
def ping_state(i):
    global ip_root, lock
    print 'state' + str(i)
    try:
        content = urllib2.urlopen("http://" + ip_root + str(i) + ":" + str(port) + "/state").read()
        with lock:
            clients[ip_root + str(i)]['master'] = True
    except:
        if ip_root + str(i) in clients:
            with lock:
                clients[ip_root + str(i)]['master'] = False

def master_pings():
    while True:
        lock.acquire()
        locked = True
        for client in clients:
            if clients[client]['master']:
            	args = client.split(':')[-1]
                lock.release()
                locked = False
                print 'test2'
                thread = threading.Thread(target=ping_state, args=(args,))
                thread.start()
                thread.join()
        if locked:
            lock.release()
        time.sleep(1)

if __name__ == '__main__':
    scan_thread = threading.Thread(target=master_scan)
    scan_thread.daemon = True
    scan_thread.start()

    ping_thread = threading.Thread(target=master_pings)
    ping_thread.daemon = True
    ping_thread.start()

    app.run(host="0.0.0.0", port=1337)


