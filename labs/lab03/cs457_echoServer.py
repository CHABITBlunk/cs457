
# TCP echo server; performs one echo and then closes and halts

import socket

HOST = '0.0.0.0'    # Listen on available IP address
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

#use "with" so we don't have to explicitly close the socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
