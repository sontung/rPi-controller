"""
This is the code for communicating with the rPi through SSH. It uses paramiko
as a main way to setup a SSH connection between this app and the rPi.
To connect successfully, one must find rPi's IP address.
"""
import paramiko
import sys
import time
import select


class SSHCommunication:
    def __init__(self):
        self.host = ""
        self.user = ""
        self.password = ""
        self.ssh = None

    def specify_information(self, host, username, password):
        """
        Specify the information for SSH.
        :param:
        :return:
        """
        self.host = host
        self.user = username
        self.password = password

    def connect(self):
        """
        Connect to the specified port.
        :return:
        """
        i = 1
        while True:
            print "Trying to connect to %s (%i/30)" % (self.host, i)

            try:
                self.ssh = paramiko.SSHClient()
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh.connect(self.host, username=self.user, password=self.password)
                print "Connected to %s" % self.host
                break
            except paramiko.AuthenticationException:
                print "Authentication failed when connecting to %s" % self.host
                sys.exit(1)
            except:
                print "Could not SSH to %s, waiting for it to start" % self.host
                i += 1
                time.sleep(2)

            # If we could not connect within time limit
            if i == 5:
                print "Could not connect to %s. Giving up" % self.host
                raise RuntimeError
                sys.exit(1)

    def disconnect(self):
        """
        Disconnect the port.
        :return:
        """
        self.ssh.close()

    def command(self, command):
        """
        Send command to bluetooth module.
        :param val:
        :return:
        """
        stdin, stdout, stderr = self.ssh.exec_command(command)

        # Wait for the command to terminate
        while not stdout.channel.exit_status_ready():
            # Only print data if there is data to read in the channel
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    # Print data from stdout
                    print stdout.channel.recv(1024),