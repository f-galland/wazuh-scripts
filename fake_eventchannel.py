#!/var/ossec/framework/python/bin/python3

import logging

logging.basicConfig(filename='/tmp/fake_eventchannel.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s')


import sys
import argparse
from socket import socket, AF_UNIX, SOCK_DGRAM


socketAddr = '/var/ossec/queue/sockets/queue'


def send_event(msg):
    logging.debug('Sending {} to {} socket.'.format(msg, socketAddr))
    sock = socket(AF_UNIX, SOCK_DGRAM)
    sock.connect(socketAddr)
    sock.send(msg.encode())
    sock.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile',help='EventChannel event as output by the EventViewer\'s "Copy Details as Text" button')
    args, namespace = parser.parse_known_args()
    logging.info(args)

    event_file = open(args.inputfile)

    header = 'f:[000] (manager) any->EventChannel:{'
    footer = '}'

    keepMessage = 0
    eventMessage = ""
    keepXML = 0
    eventXML = ""

    for line in event_file:
        if 'Event Xml:' in line:
            keepMessage = 0
        elif keepMessage == 1:
            lineBuffer = line.replace('\\','\\\\')
            lineBuffer = lineBuffer.replace('\t','\\t')
            eventMessage += lineBuffer.replace('\n','\\r\\n')
        elif 'Description:' in line:
            keepMessage = 1
        elif '<Event xmlns=' in line:
            keepXML = 1
        elif '</Event>' in line:
            keepXML = 0
            eventXML += '</Event>'
        
        
        if keepXML == 1:
            lineBuffer = line.replace('  ','')
            lineBuffer = lineBuffer.replace('\"','\'')
            eventXML += lineBuffer.replace('\n','')
    
    fakeEvent = header+'"Message":"{}","Event":"{}"'.format(eventMessage,eventXML)+footer

    send_event(fakeEvent)

    sys.exit(0)
