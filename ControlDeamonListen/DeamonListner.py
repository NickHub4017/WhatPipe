import json
import socket
from ConfigFile.ConfigParser import ConfigMonitor
import netifaces

class ControlDeamon:
    def __init__(self):  #At initilasisation phase it will read the config and config itself
        self.cm = ConfigMonitor("/home/nrv/PycharmProjects/PnpGlobalLink/ConfigFile/config.xml")
        self.ListenIP = self.cm.getIp();
        self.ListenPORT = int(self.cm.getPort())
        self.BufferSize = 1024
        self.myips = self.getAllInterfaceAddresses()


    def getAllInterfaceAddresses(self):  # get the idea of the network address of the node has.
        iplist=[]
        interface_list = netifaces.interfaces()
        for iname in interface_list:
            if (("eth" in iname) or ("wlan" in iname)): #get only eth and wlan (ethernet and wifi addresses)
                try:
                    internetIps = netifaces.ifaddresses(iname)[netifaces.AF_INET]  #fetch only IPv4 address only
                    iplist.append(internetIps[0]["addr"])
                except:
                    pass
        return iplist

    def filetrOutSelfIps(self,node):

        if(node.getip() in self.myips):
            return True
        if("127.0." in node.getip()):
            return True
        return False

    def connect(self):
        try:
            self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serversocket.bind((self.ListenIP, self.ListenPORT))
            self.serversocket.listen(1)  # Currenly listen to one
            return True
        except Exception as e:
            print e,"DemonListner @connect()"
            return False

    def handleClient(self):
        reply="********"
        while True:
            clientsock, clientaddr = self.serversocket.accept()
            print "Connection establish with client:- ", clientaddr
            totalclientdata=""
            while True:  # Will read the pipe untill no of { and no of } matches. [Parserble]
                clientdata = clientsock.recv(self.BufferSize)
                totalclientdata=totalclientdata+clientdata
                try:
                    json.loads(totalclientdata)  #Json is parsable means json is ccompletely receved
                    break
                except Exception as e:
                    print e," while capturing the json commnd string"
                    continue
            for node in self.cm.getNextNodeList(): #check all nodes sequentially for the availability
                if(not self.filetrOutSelfIps(node)):
                    print "Done"
                    self.conectToNextNode(node)
                else:
                    print "Loop detected"
            clientsock.send(reply)
            print len(reply)
            clientsock.close()

    def conectToNextNode(self,NextNode):
        try:
            NextNode.checkStatus()
            return True
        except:
            return False



c=ControlDeamon()
if(c.connect()):
    c.handleClient()