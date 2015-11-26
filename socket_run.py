import socket_example

client = socket_example.mysocket()
client.connect("192.168.43.96", 55556)
client.mysend("abc")