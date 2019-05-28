#!/usr/bin/python2

import os,commands
ip='192.168.10.218'
commands.getoutput('iptables -F')
p=commands.getoutput('iscsiadm --mode discoverydb --type sendtargets --portal '+ip+' --discover')
q=p.split()[1]
commands.getoutput('iscsiadm --mode node --targetname '+q+' --portal '+ip+':3260 --login')



