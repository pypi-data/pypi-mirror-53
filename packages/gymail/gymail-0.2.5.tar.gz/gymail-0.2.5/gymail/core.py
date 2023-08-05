#!/usr/bin/python3
"""
Use gymail as a CLI script or python module to send a mail.
See a configuration example in `$HOME/.local/share/gymail.conf`, which is created after the
first run of gymail.
"""
import argparse
import logging
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import toml
from appdirs import *
from helputils.defaultlog import log
from helputils.core import format_exception

appname = "gymail"
appauthor = "gymail"
toml_file = os.path.join(user_data_dir(appname, appauthor), "gymail.toml")
mkdir_p(user_data_dir(appname, appauthor)
log = logging.getLogger("gymail")


def create_example_config():
    example_config = (
        '# SENDER = "you@gmail.com"\n'
        '# RECIPIENT = "you@gmail.com"\n'
        '# USERNAME = "foo"\n'
        '# PASSWORD = "bar"\n'
        '# SMTP = "smtp.gmail.com:587"'
    )
    if not os.path.isfile(toml_file):
        print("(Create) example config in %s" % toml_file)
        print("(Info) Please edit the config file, then run ledger-mv")
        with open(toml_file, "w") as _file:
            _file.write(example_config)


create_example_config()
try:
    conf = toml.loads(pathlib.Path(toml_file).read_text())
except Exception as e:
    print("(Error) Please edit the config file, then run ledger-mv %s" % toml_file)
    print(format_exception(e))
    sys.exit()


def send_mail(event, subject, message, priority="low"):
    try:
        # Create message container; the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['sender'] = conf["SENDER"]
        msg['recipient'] = conf["RECIPIENT"]
        if priority == "high":
            msg['X-Priority'] = '2'
        # Escape with double curly brackets. Alternatively switch to %s string format
        style = '<style type="text/css">body {{ background-color: {0};}} p {{ color: black; font-size: 28px;}}</style>'
        error_style = style.format('red')
        warning_style = style.format('yellow')
        info_style = style.format('green')
        template = "<html>{0}<body><p>{1}</p></body></html>"
        if event.lower() in ["error", "e"]:
            html = template.format(error_style, message)
            msg['Subject'] = "error: " + subject
            log.error("Sending %s mail." % event)
        elif event.lower() in ["warning", "w"]:
            html = template.format(warning_style, message)
            msg['Subject'] = "warning: " + subject
            log.warning("Sending %s mail." % event)
        elif event.lower() in ["info", "i"]:
            html = template.format(info_style, message)
            msg['Subject'] = "info: " + subject
            log.info("Sending %s mail." % event)
        part1 = MIMEText(message, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        s = smtplib.SMTP(conf["SMTP"])
        s.starttls()
        s.login(conf["USERNAME"], conf["PASSWORD"])
        s.sendmail(conf["SENDER"], conf["RECIPIENT"], msg.as_string())
        s.quit()
    except Exception as e:
        log.error(format_exception(e))


def argparse_entrypoint():
    parser = argparse.ArgumentParser(description='Simple sendmail script.')
    parser.add_argument('-e', '--event', choices=['error', 'warning', 'info'], help='Formats html style for email accordingly.', required=True)
    parser.add_argument('-s', '--subject', help='Subject of email.', required=True)
    parser.add_argument('-m', '--msg', help='Email message goes here.', required=True)
    args = parser.parse_args()
    send_mail(args.event, args.subject, args.msg)
