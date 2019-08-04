#!/usr/bin/python2
import cgi,cgitb,commands

print "content-type:text/html"
print ""

cgitb.enable()
data=cgi.FieldStorage()
buck=data.getvalue('opt')
name=data.getvalue('nm')

web='''
</Doctype html>
<html>
<head>
	<title>MISTAKEN</title>
</head>
<body style="background-color:powderblue;">
	<h2> Oops..!! Your Bucket couldnot be created because the name has already been taken</h2>
	<p> You can try again with another name</p>
	<p> We are redirecting you to the S3 Bucket Portal</p>
	<p><a href="/aws/s3mrb.html"> Click me </a> for S3 portal</p>
</body>
</html'''

rem='''
</Doctype html>
<html>
<head>
	<title>MISTAKEN</title>
</head>
<body style="background-color:powderblue;">
	<h2> Oops..!! Your Bucket couldnot be deleted because the name does not exist</h2>
	<p> Please type in the correct name</p>
	<p> We are redirecting you to the S3 Bucket Portal</p>
</body>
</html'''

done='''
</Doctype html>
<html>
<head>
	<title>Done</title>
</head>
<body style="background-color:powderblue;">
	<p> Your request has successfully been processed </p>
	<p><a href="/aws/s3mrb.html"> Click me </a> to view your S3 buckets</p>
</body>
</html'''



if buck=="make":
	l=commands.getstatusoutput('sudo aws s3 mb s3://'+name)
	if l[0]!=0:
		print "<script>setTimeout(\"location.href='/aws/s3mrb.html';\",5000);</script>"
		print web
	else:
		print done
elif buck=="rmv":
	l=commands.getstatusoutput('sudo aws s3 rb s3://'+name+' --force')
	if l[0]!=0:
		print "<script>setTimeout(\"location.href='/aws/s3mrb.html';\",5000);</script>"
		print rem
	else:
		print done
else:
	o=commands.getoutput('sudo aws s3 ls s3://'+name+' --recursive')
	print "<pre>"+o+"</pre>"

