#!/usr/bin/python
import commands

commands.getoutput('mkdir /media/gapyt')
commands.getoutput('mount -t cifs -o username=smbgapyt //192.168.43.123/gapyt /media/gapyt')
#New SMB password:
Retype new SMB password:
Added user smbgapyt.