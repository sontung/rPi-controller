import copy
import socket_comm


holder = socket_comm.SocketCommunication()
holder.specify_information("192.168.43.96","sadf","asdf")
holder.connect()
holder.command("setRed")
copy.deepcopy(holder)