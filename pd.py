#!/usr/bin/python

import sys
import socket
from threading import Thread
import json
from Queue import Queue
import time


def check_entry(pdValDict):

    #print "PD: " ,
    for pdStr in pdValDict['clientpd']:
        message = 'announce route ' + pdStr + \
                  ' next-hop ' + pdValDict['clientaddr']
        sys.stdout.write( message + '\n')
        sys.stdout.flush()
        time.sleep(1)

def process_queue(q):
    while True:
        value = q.get()
        if ( value == 'QUIT' ):
            break 
        elif ( len(value) > 0 ):
            pdDict = json.loads(value)
            check_entry(pdDict)

def clientthread(conn,q):
    while True:
        #Receiving from client
        data = conn.recv(1024).strip()
        if not data: 
            break
        else:
            q.put(data)
     
    #came out of loop
    conn.close()

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    HOST, PORT = "localhost", 9999
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + \
               str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    my_queue = Queue()
    worker = Thread(target=process_queue, args=(my_queue,))
    worker.start()

    s.listen(10)

    while True:
        try:
            conn, addr = s.accept()
            myhandle = Thread(target=clientthread, args=(conn, my_queue,))
            myhandle.start()
        except KeyboardInterrupt:
            s.close()
            worker._Thread__stop()
            sys.exit()
