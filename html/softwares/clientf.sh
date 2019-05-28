#!/usr/bin/python2
import commands

commands.getoutput('mkdir /media/nafis')
commands.getoutput('systemctl restart rpcbind')
commands.getoutput('mount -t nfs 192.168.43.7:/mnt/nafis /media/nafis')
commands.getoutput('setenforce 0')
commands.getoutput('iptables -F')