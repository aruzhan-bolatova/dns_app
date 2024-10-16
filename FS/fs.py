from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

# Global variables to store registration information
hostname = None
ip_address = None
as_ip = None
as_port = None

@app.route('/register', methods=['PUT'])
def register():
    data = request.json
    hostname = data.get("hostname")
    ip = data.get("ip")
    as_ip = data.get("as_ip")
    as_port = int(data.get("as_port"))
    
    if not all([hostname, ip_address, as_ip, as_port]):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Register with AS via UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        message = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"
        sock.sendto(message.encode(), (as_ip, as_port))
    
    return "Registered", 201

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    try:
        number = int(request.args.get('number'))
    except ValueError:
        return "Bad format", 400
    
    def fib(n):
        if n <= 1:
            return n
        else:
            return fib(n - 1) + fib(n - 2)
    
    result = fib(number)
    return jsonify({"fibonacci": result}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9090)
