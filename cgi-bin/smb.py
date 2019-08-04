#!/usr/bin/python2

import cgi,commands
print "content-type:text/html"	
print ""
data=cgi.FieldStorage()
nam=data.getvalue('name')
siz=data.getvalue('size')
passwd=data.getvalue('passwd')
ip=commands.getoutput('sudo myipg')
commands.getoutput('sudo useradd -s /sbin/nologin '+nam)
commands.getoutput('(echo '+passwd+'; echo '+passwd+') | sudo smbpasswd -a -s '+nam) 
commands.getoutput('sudo setenforce 0')
commands.getoutput('sudo iptables -F')
commands.getoutput('sudo lvcreate --name '+nam+' --size '+siz+' myvg')
commands.getoutput('sudo mkdir /mnt/'+nam)
commands.getoutput('sudo mkfs.ext4 /dev/mapper/myvg-'+nam)
commands.getoutput('sudo mount /dev/mapper/myvg-'+nam+' /mnt/'+nam)
s='['+nam+'] '
m='path=/mnt/'+nam
k='writable=yes'
f=open('/etc/samba/smb.conf','a+')
f.write(s+' \n'+m+' \n'+k+'\n')
f.close()
commands.getoutput('sudo systemctl restart smb')
commands.getoutput('sudo iptables -F')
commands.getoutput('sudo setenforce 0')
msg="#!/usr/bin/python2\n\nimport commands\n\ncommands.getoutput(' yum install cifs-utils -y')\n\ncommands.getoutput(' yum install samba-client -y')\ncommands.getoutput('mkdir /media/"+nam+"')\ncommands.getoutput('mount -t cifs -o username="+nam+" //"+ip+"/"+nam+" /media/"+nam+"')"
k=open('/var/www/html/csmb.sh','w')
k.write(msg)
k.close()	
print '<meta http-equiv="refresh" content="text/html; url=/smbc.html" />'
