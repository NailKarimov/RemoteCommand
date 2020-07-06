# coding=utf-8
"""Command execution over SSH"""

import paramiko
from paramiko import SSHException, AuthenticationException, BadHostKeyException


class RemoteCommandException(Exception):
    pass


class RemoteCommand:
    def __init__(self, command, ssh_host, ssh_user, ssh_password=None):
        """Initialize RemoteCommand object

        :param command: Command to execute on remote host
        :param ssh_host: Remote host (IP address or domain name)
        :param ssh_user: Remote username
        :param ssh_password: password for authentication to remote host (optional in case SSH agent is used)

        Example usage:
            >>> rc = RemoteCommand("cat /proc/cmdline", "1.1.1.1", "john", "supersecretpassword")
            >>> rc.run()
            >>> rc.get_pid
            >>> rc.get_result()
        """

        self.command = command
        self.ssh_host = ssh_host
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password

        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.ssh_host, 22, self.ssh_user, self.ssh_password, timeout=5, look_for_keys=False, allow_agent=False)
        except AuthenticationException:
            print("Authentication failed, please verify your credentials: %s")
            self.client.close()
        except BadHostKeyException as badHostKeyException:
            print("Unable to verify server's host key: %s" % badHostKeyException)
            self.client.close()
        except SSHException as sshException:
            print("Unable to establish SSH connection: %s" % sshException)
            self.client.close()

    def run(self) -> None:
        """Execute command on remote host
        :raises: `RemoteCommandException` if command execution is not successful (for instance: command is not found)
        """
        try:
            (stdin, self.stdout, stderr) = self.client.exec_command('echo $$;' + self.command)
        except paramiko.SSHException:
            raise RemoteCommandException(self.command + 'command is not found')

    def get_pid(self) -> int:
        """Get PID (process ID) of executed command"""
        return int(self.stdout.readline())

    def terminate(self) -> None:
        """Terminate running command
        :raises: `RemoteCommandException` if command cannot be terminated for some reason
        """
        try:
            print('Start to terminate command ' + self.command)
            (stdin, self.stdout, self.stderr) = self.client.exec_command('kill -9 ')
        except paramiko.SSHException:
            raise RemoteCommandException('Unable to terminated process ' + self.command)

    def get_result(self) -> str:
        """Return command generated output"""
        return ''.join(self.stdout.readlines())

    def get_exit_code(self) -> int:
        """Return command exit code"""
        # running 'true' -> exit status: 0; running 'false' exit status: 1
        return int(self.stdout.channel.recv_exit_status())

    def disconnect(self) -> None:
        """Close ssh connection."""
        if self.client:
            self.client.close()


rc1 = RemoteCommand("ls -la", "10.10.1.5", "paramiko", "a123456a")
print('Run first scenario with positive result without errors: ')
rc1.run()
print("PID: " + str(rc1.get_pid()))
print(rc1.get_result())
print("Exit code is: " + str(rc1.get_exit_code()))
print('End ------------------------------------------------------')
print('')

rc2 = RemoteCommand("ls", "10.10.1.5", "paramiko", "a123456a")
print('Run second , using terminate, while command is run: ')
rc2.run()
print("PID: " + str(rc2.get_pid()))
print(rc2.get_result())
print("Exit code is: " + str(rc2.get_exit_code()))
rc2.terminate()
print("Exit code is: " + str(rc2.get_exit_code()))
print('End ------------------------------------------------------')
print('')

# rc3 = RemoteCommand("ls", "10.10.1.5", "paramiko_false_name", "a123456a")
# print('Run third scenario with invalid name: ')
# print('End ------------------------------------------------------')
# print('')

# rc3 = RemoteCommand("ls", "10.10.1.10", "paramiko", "a123456a")
# print('Run fourth scenario with invalid host: ')
# print('End ------------------------------------------------------')
# print('')

