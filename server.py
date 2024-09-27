from flask import Flask, request, jsonify

app = Flask(__name__)

# Endpoint to handle QR code data via POST requests
@app.route('/qr', methods=['POST'])
def receive_qr_code():
    # Extract QR code data from the POST request
    data = request.json.get('qr_code', None)

    if data:
        print(f"Received QR Code Data: {data}")
        # Respond with success and echo back the received data
        return jsonify({"status": "success", "data": data}), 200
    else:
        # Respond with error if no QR code data was found in the request
        return jsonify({"status": "error", "message": "No QR code data received"}), 400

if __name__ == "__main__":
    # Run the Flask app locally on port 5000
    app.run(debug=True)
