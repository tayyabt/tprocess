#Overview
This simple module allows for communication with subprocesses much like pexpect (https://pexpect.readthedocs.org/en/latest/) but it does not have the dreaded 1024 char limit for sending input to the process (http://stackoverflow.com/questions/9218499/pexpect-cant-pass-input-over-1024-chars). This is an alpha that I hacked together in a couple of hours to go around the issue described above. Right now, it just supports `sendline` and `expect`. The rest of the functionality can be added relatively easily. 

#Usage
```
from tprocess import tprocess

cmd = ... # some process command as it would be run on the shell
proc = tprocess(cmd)
proc.expect( ">", timeout = None ) # timeout is not implemented yet. 
print(proc.before) # to get the text from the subprocess stdout (and stderr)

```

#Installation

You can clone the project from GitHub or use pip.
`pip3 install git+http://github.com/tayyabt/tprocess`