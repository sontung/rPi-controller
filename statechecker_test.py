import core_communication


ssh = core_communication.SSHCommunication()
ssh.connect()
print ssh.command("cd group12; sudo python state_checker.py lights").readlines()
ssh.disconnect()
