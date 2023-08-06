# CmdPlan

**_CmdPlan_** will help you plan launch of the system commands. Just define target node name and script will search it at described nodes dictionary, but it will launch their dependencies at first.

## Requires

Python3

## Install

```bash
$ pip install cmd-plan
```
## Usage

Example:

```python
import cmd_plan

NODES = {
    'TEST': {
        'command': 'python3 manage.py runserver 127.0.0.1:8000',
    },
    'TEST_WITH_NOHUP': {
        'command': 'nohup python3 manage.py runserver 127.0.0.1:8000 >/dev/null 2>&1 &',
    },
    'SERVER_SIDE': {
        'command': './server.sh &',
    },
    'CLIENT_SIDE': {
        'command': 'python3 ./client.py',
        'dependencies': ['SERVER_SIDE', ],
    }
}

# Example 1
cmd_plan.launch('TEST', NODES)  # Run Django debug WEB-server

# Example 2
cmd_plan.launch('CLIENT_SIDE', NODES)  # Run some `client`, but run it `server` at first 
```

## License

From Russia with love.
