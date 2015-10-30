import core_communication
while True:
    client = core_communication.WebServerCommunication()
    if len(client.command("list_all")) > 0:
        print client.command("get")
