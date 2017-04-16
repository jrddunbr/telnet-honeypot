# telnet-honeypot

These scripts require python 3, and the telnet server part should probably be rewritten.

## honeypot.py

This file is the actual honeypot server. It runs on port 3333 and expects iptables to redirect 23 to 3333.

It creates logs in /logs, which are IP~TIMESTAMP.log

## login.py

This file reads the logs from the honeypot server. It exepcts files in logs and then reads all the usernames and passwords, and spits them out to the console in a counted list.
