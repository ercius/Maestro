# Button pusher server

import socket
from TEAM05_tia_gatan import set_TIA2, set_Gatan

HOST = '131.243.3.206'  # Standard loopback interface address (team05-support)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

set_TIA2()
TIA = True

print('Start listening')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            print(data)
            if not data:
                break
            if data.decode() == 'gatan' and TIA:
                set_Gatan()
                TIA = False
            elif data.decode() == 'tia' and not TIA:
                set_TIA2()
                TIA = True
            conn.sendall(data)

print('Disconnected')