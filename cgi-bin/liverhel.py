#!/usr/bin/python2
import cgi
import os
import commands
import time
import json


print "Content-Type:text/html\n"
print ""

data=cgi.FieldStorage()
dirname=data.getvalue('dname')
dirram=data.getvalue('dram')
dircpu=data.getvalue('dcpu')

#print dirname,dirram,dircpu



commands.getoutput('sudo qemu-img create -f qcow2 -b /var/lib/libvirt/images/rhvmdnd.qcow2 /var/lib/libvirt/images/'+dirname+'.qcow2')


print os.system('sudo virt-install --name '+dirname+' --ram '+dirram+' --vcpu '+dircpu+' --os-variant rhel7 --disk path=/var/lib/libvirt/images/'+dirname+'.qcow2 --graphics vnc,listen=192.168.10.111,port=6200,password=abhi --import --noautoconsole &')

time.sleep(5)

os.system('sudo websockify --web=/usr/share/novnc 6300 192.168.10.111:6200 &')

print "donnewebsock"


os.system('sudo qr http://192.168.10.111:6300 > /var/www/html/iaas/images/'+dirname+'.png')


print "novnc"

web='''
<!DOCTYPE html>
<html lang="en">
<head>
  <title>IAAS CLOUD</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="/static/template1.css">
  <script src="/static/template2.js"></script>
  <script src="/static/template3.js"></script>
</head>
<body style="background-color:powderblue">
<div class="container">
  <h1 style="color:red">IAAS CLOUD</h1>
  <div class="list-group">
    <a href='http://192.168.1.100:7000'>Here is your OS</a><br><br>
    <a href=../iaas/images/'''+dirname+'''.png>You can also use the OS on phone by scanning the generated QR code</a>
  </div>
</div>

</body>
</html>
'''

print web
