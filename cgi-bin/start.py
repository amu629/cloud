#!/usr/bin/python2

import socket,commands,os,time
import cgi
print "content-type:text/html"		
d=cgi.FieldStorage()
data=d.getvalue('name')
dat=d.getvalue('size')
commands.getoutput('sudo systemctl start nfs-server')
commands.getoutput('sudo systemctl start rpcbind')
commands.getoutput('sudo mkdir /mnt/'+data)
#commands.getoutput('sudo lvcreate --name '+data+' --size '+dat+' myvg')
#commands.getoutput('sudo mkfs.ext4 /dev/mapper/myvg-'+data)
#commands.getoutput('sudo mount /dev/mapper/myvg-'+data+' /mnt/'+data)
msg='/mnt/'+data+' *(rw,no_root_squash,fsid=0) \n'
f=open('/etc/exports','a+')
f.write(msg)
f.close()
commands.getoutput('sudo iptables -F ; sudo setenforce=0')
commands.getoutput('sudo systemctl restart rpcbind')
commands.getoutput('sudo systemctl restart nfs-server')
commands.getoutput('sudo systemctl enable nfs-server')
commands.getoutput('sudo exportfs -r')
ip=commands.getoutput('sudo myip')

msg="#!/usr/bin/python2\nimport commands\n\ncommands.getoutput('mkdir /media/"+data+"')\ncommands.getoutput('mount -t nfs "+ip+":/mnt/"+data+" /media/"+data+"')\ncommands.getoutput('setenforce 0')\ncommands.getoutput('iptables -F')"

k=open('/var/www/html/clientf.sh','w')
k.write(msg)
k.close()


web='''
<!Doctype html>
<html>
	<head>
		<title> SUCCESSFUL COMPLETION </title>
	</head>
	<body>
		<h1> Woohooo..!! Its almost ready now </h1>
		<p> Just follow the steps below and u can enjoy our service</p>
		<ol>
			<li>CLick on the following link to download the executable code 			
			<br> <a href="/clientf.sh"> Click me </a> </li>
			<li>Double click on the file to run it</li>
		</ol>
		<h1> Congrats u hv done it ...!!!</h1>
	</body> 
</html>
'''	
print web



