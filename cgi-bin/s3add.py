#!/usr/bin/python2
import cgi,commands,time
print "content-type:text/html"
print ""
data=cgi.FieldStorage()
buck=data.getvalue('opt')
bnm=data.getvalue('s1')
nm=data.getvalue('s2')


if buck=="fil":
	commands.getoutput("sudo aws s3 cp "+nm+" s3://"+bnm)
else:
	commands.getoutput("sudo aws s3 sync "+nm+" s3://"+bnm)


done='''
</Doctype html>
<html>
<head>
	<title>Done</title>
</head>
<body style="background-color:powderblue;">
	<p> Your request has successfully been processed </p>
	<p><a href="/aws/s3show.html"> Click me </a> to view your S3 bucket content</p>
</body>
</html'''

print done
