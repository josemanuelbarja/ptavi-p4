#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import sys

# Constantes. Dirección IP del servidor y contenido a enviar
try:
    SERV_IP = sys.argv[1]
    SERV_PORT = int(sys.argv[2])
    METHOD = str.upper(sys.argv[3])
    ID = sys.argv[4]
    EXPIRES = sys.argv[5]
except:
    sys.exit('Usage: python client.py ip port register sip_address expires')

WORDS = (METHOD + ' sip:' + ID + ' SIP/2.0\r\n'
+ 'Expires: ' + EXPIRES + '\r\n\r\n')

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERV_IP, SERV_PORT))
    print('Sending: ' + ' '.join(WORDS.split('\r\n')))
    my_socket.send(bytes(WORDS, 'utf-8'))
    try:
        data = my_socket.recv(1024)
        print('Recived:', data.decode('utf-8'))
    except:
        sys.exit('Connection Refused: No server listening at: ' + SERV_IP +
        ':' + str(SERV_PORT))

print("Socket terminado.")
