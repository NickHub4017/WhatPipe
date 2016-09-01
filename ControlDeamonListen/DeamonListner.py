import socket
from ConfigFile.ConfigParser import ConfigMonitor
import netifaces

class ControlDeamon:
    def __init__(self):
        self.cm = ConfigMonitor("/home/nrv/PycharmProjects/PnpGlobalLink/ConfigFile/config.xml")
        self.ListenIP = self.cm.getIp();
        self.ListenPORT = int(self.cm.getPort())
        self.BufferSize = 1024
        self.myips = self.getAllInterfaceAddresses()  #get the idea of the network address of the node has.


    def getAllInterfaceAddresses(self):
        iplist=[]
        interface_list = netifaces.interfaces()
        for iname in interface_list:
            if (("eth" in iname) or ("wlan" in iname)):
                try:
                    internetIps = netifaces.ifaddresses(iname)[netifaces.AF_INET]
                    iplist.append(internetIps[0]["addr"])
                except:
                    pass
        return iplist

    def connect(self):
        try:
            self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serversocket.bind((self.ListenIP, self.ListenPORT))
            self.serversocket.listen(1)  # Currenly listen to one

            return True
        except:
            return False

    def handleClient(self):
        reply="********"
        while True:
            clientsock, clientaddr = self.serversocket.accept()
            print "Connection establish with client:- ", clientaddr

            while True:
                clientdata = clientsock.recv(self.BufferSize)
                if (not clientsock):
                    break
                for node in self.cm.getNextNodeList():
                    self.conectToNextNode(node)
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
#c.connect()
#c.handleClient()