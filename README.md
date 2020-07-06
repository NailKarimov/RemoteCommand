# Python homework: RemoteCommand

You are given wire-frame API as defined in `remcmd.py`. Your task is to
implement missing functionality in `RemoteCommand` class. This class implements
simple API for executing arbitrary command on remote host accessible over SSH
connection.

Please do following:
```
1. Choose readily available Python SSH library.
2. Implement all missing methods in `RemoteCommand` class.
3. Write tests for this API.
```

There are several tests, which may run during testing this API, some example:

Positive tests:
```
  Try to connect to the remote host, check if is available, and SSH port must be configured on the remote.
  Connect, using  correct ssh_host, ssh_user, ssh_password
  Try to run a simple command like "ls" or "ls -la" to check the output result
  Use the "Terminate" method to kill the running process
  Check "pid" while command start to run, terminate
  Check "exit code", when command finished by itself and after termination if they:
    running 'true' -> exit status: 0; running 'false' exit status: 1
```

Negative tests:
```
  Host is wrong
  Host not support SSH connection
  Execute the wrong command to see Exception outputs
  Make first authorization with newly generated keys, without using "paramiko.AutoAddPolicy()"
  Try to run the script, while this user already authorized, for example via "Putty"
  ```

Some examples from code:

1. Connect, using  correct ssh_host, ssh_user, ssh_password, run "ls -la", get "pid", get exit code:
```
rc1 = RemoteCommand("ls -la", "10.10.1.5", "paramiko", "a123456a")
print('Run first scenario with positive result without errors: ')
rc1.run()
print("PID: " + str(rc1.get_pid()))
print(rc1.get_result())
print("Exit code is: " + str(rc1.get_exit_code()))
print('End ------------------------------------------------------')
print('')
```

Output:

C:\Users\karim\Downloads\Homework>remcmd.py
Run first scenario with positive result without errors:
PID: 6371
total 8
drwxr-xr-x 2 paramiko users 4096 Jul 6 11:22 .
drwxr-xr-x 7 root root 4096 Jul 6 11:22 ..

Exit code is: 0
End ------------------------------------------------------


2. Connect, using  correct ssh_host, ssh_user, ssh_password, run "ls", get "pid", get exit code, terminate command, get exit code,
```
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
```
Output:

Run second , using terminate, while command is run:
PID: 6394

Exit code is: 0
Start to terminate command ls
Exit code is: 1
End ------------------------------------------------------

3. Connect, using  incorrect ssh_host, ssh_user, ssh_password
```
# rc3 = RemoteCommand("ls", "10.10.1.5", "paramiko_false_name", "a123456a")
# print('Run third scenario with invalid name: ')
# print('End ------------------------------------------------------')
# print('')

# rc4 = RemoteCommand("ls", "10.10.1.10", "paramiko", "a123456a")
# print('Run fourth scenario with invalid host: ')
# print('End ------------------------------------------------------')
# print('')
```
