#!/usr/bin/python

import cgi,commands
print "content-type:text/html"
print ""
obj=cgi.FieldStorage()
d_name=obj.getvalue('name')
d_size=obj.getvalue('size')
commands.getoutput('sudo systemctl start nfs-server')
commands.getoutput('sudo systemctl start rpcbind')
commands.getoutput('sudo lvcreate --name '+d_name+' --size '+d_size+' vg')
commands.getoutput('sudo mkfs.xfs /dev/vg/'+d_name)
commands.getoutput('sudo mkdir /mnt/'+d_name)
commands.getoutput('sudo mount /dev/vg/'+d_name+' /mnt/'+d_name)
msg='/mnt/'+data+'	*(rw,no_root_squash,fsid=0)
f=open('etc/fstab','+a')
f.write(msg)
f.close()
commands.getoutput('sudo iptables -F ; sudo setenforce=0')
commands.getoutput('sudo systemctl restart rpcbind')
commands.getoutput('sudo systemctl restart nfs-server')
commands.getoutput('sudo systemctl enable nfs-server')
commands.getoutput('sudo exportfs -r')

