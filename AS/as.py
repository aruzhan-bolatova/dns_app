import socket

dns_records = {}

def handle_registration(message):
    lines = message.split("\n")
    hostname, ip = None, None
    for line in lines:
        if line.startswith("NAME="):
            hostname = line.split("=")[1]
        elif line.startswith("VALUE="):
            ip = line.split("=")[1]
    
    if hostname and ip:
        dns_records[hostname] = ip
        return f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"
    else:
        return "Error: Invalid registration message"

def handle_query(message):
    lines = message.split("\n")
    hostname = None
    for line in lines:
        if line.startswith("NAME="):
            hostname = line.split("=")[1]
            break
    
    if hostname and hostname in dns_records:
        ip = dns_records[hostname]
        return f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"
    else:
        return "Error: Hostname not found"

def handle_client(data, client_address):
    message = data.decode()
    if "TYPE=A" in message and "VALUE" in message:
        response = handle_registration(message)
    else:
        response = handle_query(message)
    return response.encode()

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 53533))
    print("Authoritative Server is running on port 53533...")

    while True:
        data, client_address = server_socket.recvfrom(1024)
        response = handle_client(data, client_address)
        server_socket.sendto(response, client_address)

if __name__ == "__main__":
    run_server()