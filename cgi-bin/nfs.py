#!/usr/bin/python

import cgi,commands
print "content-type:text/html"
print ""
obj=cgi.FieldStorage()
d_name=obj.getvalue('name')
d_size=obj.getvalue('size')

#commands.getoutput('sudo lvcreate --name '+d_name+' --size '+d_size+' vg')
#commands.getoutput('sudo mkfs.xfs /dev/vg/'+d_name)
a=commands.getoutput('sudo mkdir /mnt/'+d_name)
#commands.getoutput('sudo mount /dev/vg/'+d_name+' /mnt/'+d_name)


msg='\n/mnt/'+d_name+'	*(rw,no_root_squash,fsid=0)\n'
f=open('/etc/exports','a+')
f.write(msg)
f.close()


commands.getoutput('sudo iptables -F ; sudo setenforce=0')
commands.getoutput('sudo systemctl restart rpcbind')
commands.getoutput('sudo systemctl restart nfs-server')
commands.getoutput('sudo systemctl enable nfs-server')
commands.getoutput('sudo exportfs -r')

ip=commands.getoutput('myipg')

msg='#!/usr/bin/python\nimport commands\n\ncommands.getoutput(\'mkdir /media/'+d_name+'\')\ncommands.getoutput(\'mount -t nfs '+ip+':/mnt/'+d_name+' /media/'+d_name+'\')'

f=open('/var/www/html/nfs_share.py','w')
f.write(msg)
f.close()


web = '''
<!Doctype html>
<html>
	<head>
		<title>SUCCESSFUL COMPLETION'''+a+'''</title>
	</head>
	<body>
		<h1>DONE</h1>
		<p> <a href="/nfs_share.py" download>Click me</a> </p>
	</body>
</html>
'''
print web






