#!/usr/bin/python2
import cgi,commands
print "content-type:text/html"
print ""
data=cgi.FieldStorage()
name=data.getvalue('nm')



l=commands.getstatusoutput('sudo aws s3 website s3://'+name+'/ --index-document index.html ')

link="http://"+name+".s3-website-ap-south-1.amazonaws.com/"
done='''
</Doctype html>
<html>
<head>
	<title>Static Web Hosting</title>
</head>
<body style="background-color:powderblue;">
	<p> Your request has successfully been processed </p>
	<p> You can visit your site by going to the following link -- '''+link+'''</p>
</body>
</html'''
print done
