#!/usr/bin/python2

import commands

commands.getoutput(' yum install cifs-utils -y')

commands.getoutput(' yum install samba-client -y')
commands.getoutput('mkdir /media/sambhu')
commands.getoutput('mount -t cifs -o username=sambhu //192.168.10.218/sambhu /media/sambhu')
