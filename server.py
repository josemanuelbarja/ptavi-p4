#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socketserver
import sys
import json
import time

class SIPRegisterHandler(socketserver.DatagramRequestHandler):

    usr = {}

    def json2register(self):
        try:
            with open(JSON_FICH, 'r') as filejson:
                self.usr = json.load(filejson)
        except:
            pass

    def register2json(self,fich):
        with open(fich, 'w') as filejson:
            json.dump(self.usr,filejson,indent = 4)

    def handle(self):
        line = self.rfile.read()
        linedecod = line.decode('utf-8')
        self.message = linedecod.split('\r\n')
        print("Received:", ' '.join(self.message))
        self.sip_register()

    def sip_register(self):
        IP = self.client_address[0]
        try:
            method = self.message[0].split(' ')[0]
            expires = int(self.message[1].split(': ')[1])
        except:
            sys.exit('Bad Request')
        if method == 'REGISTER':
            deadtime = time.gmtime(time.time()+ 3600 + expires)
            strdeadtime = time.strftime('%d/%m/%Y %H:%M:%S', deadtime)
            sip_address = self.message[0].split(' ')[1].split(':')[1]
            if expires > 0:
                usr_data = {'serverport': IP,
                            'expires': strdeadtime}
                self.usr[sip_address] = usr_data
                self.wfile.write(bytes(COD_OK,'utf-8'))
            elif expires == 0:
                try:
                    del self.usr[sip_address]
                    self.wfile.write(bytes(COD_OK,'utf-8'))
                except:
                    print('User Not Found')
        else:
            print('Method Not Allowed')
        self.register2json(JSON_FICH)


if __name__ == "__main__":
    try:
        PORT = sys.argv[1]
    except:
        sys.exit('Usage: python server.py port')
    COD_OK = 'SIP/2.0 200 OK\r\n\r\n'
    JSON_FICH = 'registered.json'
    serv = socketserver.UDPServer(('', int(PORT)), SIPRegisterHandler)
    print("Server listening at 127.0.0.1:" + PORT)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
