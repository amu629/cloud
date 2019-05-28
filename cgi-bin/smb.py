#!/usr/bin/python

import cgi,commands
print "content-type:text/html"
print ""
obj=cgi.FieldStorage()
d_name=obj.getvalue('name')
d_size=obj.getvalue('size')
u_name = 'smb'+d_name
d_pass=obj.getvalue('passwd')

#commands.getoutput('sudo lvcreate --name '+d_name+' --size '+d_size+' vg')
#commands.getoutput('sudo mkfs.xfs /dev/vg/'+d_name)
commands.getoutput('sudo mkdir /mnt/'+d_name)
#commands.getoutput('sudo mount /dev/vg/'+d_name+' /mnt/'+d_name)
commands.getoutput('sudo useradd -s /sbin/nologin '+u_name)
commands.getoutput('(echo '+d_pass+';echo '+d_pass+') | sudo smbpasswd -a '+u_name)

msg='\n['+d_name+']\npath = /mnt/'+d_name+'\nbrowseable = Yes\nwriteable = Yes\n'
f=open('/etc/samba/smb.conf','a+')
f.write(msg)
f.close()


commands.getoutput('sudo iptables -F ; sudo setenforce=0')
commands.getoutput('sudo systemctl restart smb')
commands.getoutput('sudo systemctl enable smb')

ip=commands.getoutput('myipg')

msg='#!/usr/bin/python\nimport commands\n\ncommands.getoutput(\'mkdir /media/'+d_name+'\')\ncommands.getoutput(\'mount -t cifs -o username='+u_name+' //'+ip+'/'+d_name+' /media/'+d_name+'\')\n'

f=open('/var/www/html/smb_share.py','w')
f.write(msg)
f.close()


web = '''
<!Doctype html>
<html>
	<head>
		<title>SUCCESSFUL COMPLETION</title>
	</head>
	<body>
		<h1>DONE</h1>
		<p> <a href="/smb_share.py" download>Click me</a> </p>
	</body>
</html>
'''
print web





