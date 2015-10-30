import core_communication


ssh = core_communication.SSHCommunication()
ssh.connect()
print ssh.command("ls").readlines()
print ssh.command("cd light_control; sudo python state_checker.py lights").readlines()
ssh.disconnect()
