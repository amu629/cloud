#!/usr/bin/python
import commands

commands.getoutput('mkdir /media/redd')
commands.getoutput('mount -t nfs 192.168.43.123:/mnt/redd /media/redd')