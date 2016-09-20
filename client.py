#!/usr/bin/env python 

""" 
A simple JSON over sockets client
""" 

import socket 
import sys

host = 'localhost' 
port = 9999 
size = 1024 

clientmac = '\"clientmac\": \"{}\",'.format(sys.argv[1])
clientaddr = '\"clientaddr\": \"{}\",'.format(sys.argv[2])
clientpd = '\"clientpd\": {} \"{}\": {} {}'.format('{',
                                               sys.argv[3],
                                               '{ }',
                                               '}',
                                              )

pdinfo = '{} {} {} {} {}'.format('{',
                                 clientmac,
                                 clientaddr,
                                 clientpd,
                                 '}',
                                 ) 
#pdinfo = '{ ' + \
#           '"clientmac": "' + sys.argv[1] + '", ' + \
#           '"clientaddr": "' + sys.argv[2] + '", ' + \
#           '"clientpd": ' + \
#              '{ "' + \
#                sys.argv[3] + '": { } ' + \
#              '} ' + \
#         '}'

# A simple logging mechanism to /tmp
fh = open('/tmp/mylog.txt','w')
fh.write(pdinfo)
fh.close()

if ( len(sys.argv[3]) > 1):            
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect((host,port)) 
    s.send(pdinfo) 
    s.close()
else:
    sys.exit(0)
