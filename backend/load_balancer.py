import requests
from config import SERVERS, LOAD_BALANCING_ALGORITHM
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

def health_check(server):
    try:
        response = requests.get(f"http://{server['host']}:{server['port']}/health")
        return response.status_code == 200
    except:
        return False

# Global variable to keep track of the current server index
current_server_index = 0

def get_next_server(algorithm, servers):
    global current_server_index

    if not servers:
        return None

    if algorithm == 'round_robin':
        # Select the next server in a cyclic manner
        next_server = servers[current_server_index]
        current_server_index = (current_server_index + 1) % len(servers)
        return next_server
    
    elif algorithm == 'least_connections':
        # Implement least connections algorithm
        pass
    elif algorithm == 'ip_hash':
        # Implement IP hash algorithm
        pass

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send_operation')
def handle_operation(operation):
    healthy_servers = [server for server in SERVERS if health_check(server)]
    next_server = get_next_server(LOAD_BALANCING_ALGORITHM, healthy_servers)

    if next_server is None:
        emit('result', {'error': 'No healthy servers available'})
        return

    try:
        response = requests.post(f"http://{next_server['host']}:{next_server['port']}/calculate", json={'operation': operation})
        data = response.json()
        emit('result', data)
    except Exception as e:
        emit('result', {'error': str(e)})

if __name__ == '__main__':
    socketio.run(app, port=8080)