import dpkt
import sys
import time
    def main():
        myFile = open(sys.argv[1],'rb')
        pcap = dpkt.pcap.Reader(myFile)
        numRequest = {}    #keeps track of the # of requests sent and the ips
        numResponse = {}   #keeps track of the # of responses recieved and the ips
        

        for ts, buf in pcap:
            try :
                ethernetVar = dpkt.ethernet.Ethernet(buf)
                if ethernetVar.type != dpkt.ethernet.ETH_TYPE_IP:
                    continue
                ip = ethernetVar.data
                if ip.p != dpkt.ip.IP_PROTO_TCP:
                    continue
                tcp = ip.data
                if (tcp.flags & dpkt.tcp.TH_SYN) and not (tcp.flags & dpkt.tcp.TH_ACK):
                    numRequest[ip.src] = numRequest.get(ip.src,0) + 1

                elif ((tcp.flags & dpkt.tcp.TH_SYN) and (tcp.flags & dpkt.tcp.TH_ACK)):
                    numResponse[ip.dst] = numResponse.get(ip.dst,0) + 1
            except dpkt.dpkt.NeedData:
                continue


        finalKeys = list(numRequest.keys())	
        for i in finalKeys:
            if numRequest[i] > 3 * numResponse.get(i,0):
                print(str(i[0])+"."+str(i[1])+"."+str(i[2])+"."+str(i[3]))


if __name__ == '__main__':
    main()