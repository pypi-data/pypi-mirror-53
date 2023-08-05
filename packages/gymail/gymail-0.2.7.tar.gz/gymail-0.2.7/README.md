# gymail
gymail is a simple python mail notification script with three eligible event types
(error, warning and info), for each a different visual style is applied in an HTML body.
Use it as a script or a python module.

## Install
`pip install gymail`

## Configuration:
After running gymail the first time, a config example is created in
`~/.local/share/gymail/gymail.toml`

## CLI
- Example: `gymail.py -e info -s Backup -m "Backup was successful"`

### Usage
``` 
usage: gymail.py [-h] -e {error,warning,info} -s SUBJECT -m MSG

Simple sendmail script.

optional arguments:
  -h, --help            show this help message and exit
  -e {error,warning,info}, --event {error,warning,info}
                        Formats html style for email accordingly.
  -s SUBJECT, --subject SUBJECT
                        Subject of email.
  -m MSG, --msg MSG     Email message goes here.
```

## Module usage:
```
from gymail.core import send_mail
send_mail(event="error", message="foo", subject="example")
send_mail(event="info", message="foo", subject="example")
send_mail(event="warning", message="foo", subject="example")
```
