#!/usr/bin/python2
import cgi
import os
import commands
import time

print "content-type:text/html"
print ""
data=cgi.FieldStorage()
dirname=data.getvalue('dname')
dirram=data.getvalue('dram')
dircpu=data.getvalue('dcpu')

os.system('sudo qrencode -s 8*8 -o /var/www/html/images/wow.png http://192.168.1.100:6087')
#os.system('sudo qemu-img create -f qcow2 -b /var/lib/libvirt/images/rhcsa_exam.qcow2 /var/lib/libvirt/images/'+dirname+'.qcow2')
os.system('sudo virt-install --name '+dirname+' --ram '+dirram+' --vcpu '+dircpu+' --disk path=/var/lib/libvirt/images/manka.qcow2 --graphics vnc,listen=0.0.0.0,port=5964 --import &')
os.system('sudo websockify --web=/usr/share/novnc 6087 0.0.0.0:5964 &')

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
    <a href='http://192.168.1.100:6087'>Here is your OS</a><br><br>
    <a href='/images/wow.png'>You can also use the OS on phone by scanning the generated QR code</a>
  </div>
</div>

</body>
</html>
'''

print web
