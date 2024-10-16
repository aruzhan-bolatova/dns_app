from flask import Flask, request
import requests
import socket

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    # Extract parameters from the request
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = int(request.args.get('as_port'))
    
    # Check if all parameters are present
    if not all([hostname, fs_port, number, as_ip, as_port]):
        return "Missing parameters", 400
    
    # Send DNS query to AS; Query AS to get IP for hostname
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(f"TYPE=A\nNAME={hostname}\n".encode(), (as_ip, as_port))
            data, _ = sock.recvfrom(1024)
            response = data.decode().split("\n")
            ip = None
            for line in response:
                if line.startswith("VALUE="):
                    ip = line.split("=")[1]
            if not ip:
                return "Hostname not found", 400
            
            # Query Fibonacci Server
            fs_url = f"http://{ip}:{fs_port}/fibonacci?number={number}"
            result = requests.get(fs_url)
            return result.text, result.status_code
            
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
