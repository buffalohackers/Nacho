from flask import Flask, request
import json, time, threading, urllib2

app = Flask(__name__)
app.debug = True

print 'init'
masters = {}
clients = {}
idle_checking = False
master_scanning = False
ip_root = 'http://10.0.0.'
port = '1337'

@app.route('/state')
def connect():
    global clients, idle_checking, master_scanning
    if request.remote_addr in clients:
        clients[request.remote_addr]['timestamp'] = time.time()
    else:
        clients[request.remote_addr] = {
            'timestamp': time.time(),
            'stream': '',
            'volume': 50
        }
    
    if not idle_checking:
        thread = threading.Thread(target=disconnect_idles)
        thread.start()

        idle_checking = True

    if not master_scanning:
        thread = threading.Thread(target=master_scan)
        thread.start()

        master_scanning = True

    return json.dumps(clients[request.remote_addr])

@app.route('/clients')
def get_clients():
    return json.dumps(clients)

@app.route('/')
def helo():
    return "hello world"

def disconnect_idles():
    while len(clients) > 0:
        clients_to_pop = []
        for client in clients:
            if (time.time() - clients[client]['timestamp'] > 10):
                clients_to_pop.append(client)
        for client in clients_to_pop:
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
        print "Masters:"
        for master in masters:
            print master
        time.sleep(10)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1337)
