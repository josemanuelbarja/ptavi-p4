#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys

server = bytes(sys.argv[1], 'utf-8')


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    tags = {'address': ''}

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        self.wfile.write(b"Hemos recibido tu peticion")
        list = []
        for line in self.rfile:
            list.append(line.decode('utf-8'))
            data = list[0].split(' ')
        print("El cliente nos manda ", list[0])
        data = [data[1].split(':')[1]]
        self.tags['address'] = self.client_address[0]
        data[0].append(self.tags)
        print("IP y puerto del cliente: {}".format(self.client_address) + '\n')
        print(data[0])

if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request
    serv = socketserver.UDPServer(('', int(server)), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
