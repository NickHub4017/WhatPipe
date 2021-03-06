import socket



class inputDaemon:
    def __init__(self):
        self.ip=''
        self.port=8100
        self.bufferSize=1024

    def connect(self): #Bind the Socket
        try:
            self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serversocket.bind((self.ip, self.port))
            self.serversocket.listen(1)
            return True
        except Exception as e:
            print e, "InputDaemon @connect()"
            return False

    def handleClient(self):
        while True:
            clientsock, clientaddr = self.serversocket.accept()
            while True:  # Will read the pipe untill no of { and no of } matches. [Parserble]
                msg = clientsock.recv(self.bufferSize)
                print msg
            clientsock.close()


