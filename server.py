from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app)

# Endpoint to handle QR code data via POST requests
@app.route('/qr', methods=['POST'])
def receive_qr_code():
    data = request.json.get('qr_code', None)
    if data:
        print(f"Received QR Code Data: {data}")
        socketio.emit('qr_code_received', {'data': data})
        return jsonify({"status": "success", "data": data}), 200
    else:
        return jsonify({"status": "error", "message": "No QR code data received"}), 400

# Serve the website displaying QR codes
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>QR Code Scanner</title>
        <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
        <script type="text/javascript" charset="utf-8">
            var socket = io.connect('http://' + document.domain + ':' + location.port);
            socket.on('qr_code_received', function(data) {
                document.getElementById('qr_code').innerText = 'Scanned QR Code: ' + data.data;
            });
        </script>
    </head>
    <body>
        <h1>Real-Time QR Code Scanner</h1>
        <p id="qr_code">Waiting for QR Code...</p>
    </body>
    </html>
    '''

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
