import core_communication
while True:
    client = core_communication.WebServerCommunication(3875, "7IW3BGP1IT0FOGYQ")
    if len(client.command("list_all")) > 0:
        print client.command("get")
