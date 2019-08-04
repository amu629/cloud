#!/usr/bin/python2
import cgi,commands,time
print "content-type:text/html"
print ""
data=cgi.FieldStorage()
iid=data.getvalue('iid')
name=data.getvalue('name')
region="us-west-2"

ami_snap=commands.getoutput("sudo aws ec2 create-image --instance-id "+iid+" --name "+name+" --description 'An AMI for my server' --query 'ImageId'")


m=iid+" "+ami_snap

time.sleep(10)

f=open("/var/www/html/ec2back.txt",'a+')
f.write(m+"\n")
f.close()

web='''
<!Doctype html>
<html>
<head>
	<title>Backup Volume</title>
</head>
<body style="background-color:powderblue;">
	<h1> We have successfully processed your request</h1>
	<br>
	<p> The backup for your instance requested by you has successfully been made </p>
	<p> Please note down the details of your snapshot instance image </p>
	<ul> 
		<li>Volume Id :'''+iid+'''</li>
		<li>Snapshot Id : '''+ami_snap+'''<li>
		<li>Name of your Image: '''+name+'''<li>
		<li>To launch an instance from the snap-shot of yur ami , click on the following link <a href="/aws/ec2bl.html"> Launch Instance from Image </a> and make sure you have the info about the Snapshot ID so that instance can be launched</li>
		<li> You can do this step later also. We have created an option for that </li>
	</ul>
</body>
</html>'''

print web


