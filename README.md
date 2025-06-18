# Stealthy Webshell

## Server Side
Written in PHP, has some basic upload functionality.

## Client Side
Python

## Usage

### Command Execution
```
/bin/python client_obf.py [URL] [name of the webshell file on server]
```

#### Example:
```
/bin/python client_obf.py https://yourwebsite.local whatever.php
```

It is made for a specific purpose - you may want to change the source code. 

### File Upload
```
/bin/python client_obf.py https://yourwebsite.local whatever.php --upload /usr/bin/nxc --remote-path /tmp/nxc 
```
