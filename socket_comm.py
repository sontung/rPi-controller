import socket
import routines


class SocketCommunication:
    def __init__(self):
        self.host = ""
        self.username = ""
        self.password = ""
        self.hostPort = 55556
        self.timeout = 5
        self.sendRoutines, self.receiveRoutine = None, None

    def specify_information(self, host, username, password, mkey=b"asdf"):
        self.host=host
        self.username=username
        self.password=password
        self.sendRoutines, self.receiveRoutines = routines.initRoutines(mkey)

    def connect(self):
        _socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        _socket.connect((self.host, self.hostPort))
        _socket.settimeout(self.timeout)
        _socket.shutdown(socket.SHUT_RDWR)
        _socket.close()

    def command(self, command):
        _socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        _socket.connect((self.host, self.hostPort))
        _socket.settimeout(self.timeout)

        command=command.encode()
        rv=self.sendRoutines.toBeExecuted(command, _socket)

        _socket.shutdown(socket.SHUT_RDWR)
        _socket.close()
        print(rv)
