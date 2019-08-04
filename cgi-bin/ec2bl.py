#!/usr/bin/python2
import cgi,commands
print "content-type:text/html"
print ""
data=cgi.FieldStorage()
sg=data.getvalue('sg')
ami_id=data.getvalue('sid')
cnt=data.getvalue('cnt')
key_pair="mykey"
key_pair_path="/root/Desktop/mykey.pem"
w="ami-c2c3a2a2"
need=" "
f=open("/var/www/html/ec2back.txt","r")
for b in f:
	if b.split()[1]=='"'+ami_id+'"':
		need=b.split()[0]
		break
f.close()

ami=""
k=open("/var/www/html/ec2os.txt","r")
for c in k:
	if c.split()[1]=='"'+need+'"':
		ami=c.split()[0]
		break
k.close()

sec_id=commands.getoutput('sudo aws ec2 create-security-group --group-name '+sg+' --description "security group for development environment in EC2" --query "GroupId"')

if ami!=w:
	commands.getoutput('sudo aws ec2 authorize-security-group-ingress --group-name '+sg+' --protocol tcp --port 22 --cidr 0.0.0.0/0')

launch_instance_id=commands.getoutput('sudo aws ec2 run-instances --image-id '+ami_id+' --security-group-ids '+sec_id+' --count '+cnt+' --instance-type t2.micro --key-name '+key_pair+' --query "Instances[0].InstanceId"')

pub_ip=commands.getoutput('sudo aws ec2 describe-instances --instance-ids '+launch_instance_id+' --query "Reservations[0].Instances[0].PublicIpAddress"')

if ami==w:
	# GET THE PASSWORD FOR WINDOWS INSTANCE
	passwd=commands.getoutput('sudo aws ec2 get-password-data --instance-id  '+launch_instance_id+' --priv-launch-key '+key_pair_path+' --query "PasswordData"')


web='''
<!Doctype html>
<html>
<head>
	<title>yoyoyoy</title>
</head>
<body style="background-color:powderblue;">
	<h1> We have successfully processed your request</h1>
	<br>
	<p> Just follow the instructions to get access to your instance </p>
	<p> Please note down the following details related to your instance </p>
	<ul> For Linux Instances
		<li>Image Id :'''+ami_id+'''</li>
		<li>Instance Id-- '''+launch_instance_id+'''</li>
		<li>Public IP -- '''+pub_ip+'''</li>
		<li><a href="/mykey.pem"> Download this </a> file to get the access key-pair file</li>
		<li>To access instance, give the full path of the file you downloaded</li>
	</ul>
	<p> Please "ssh" to the instance launched by you in the following manner..</p>
	<br>
	<p>" ssh -i path_of_downloaded_file/downloaded_file_name     user_name@public_ip_of_instance</p>
	<p> REDHAT USERNAME is ec2-user </p>
	<p> UBUNTU USERNAME is ubuntu </p>
	<ul> For WINDOWS Instances
		<ul>Please note down the following things:
			<li> Instance ID: '''+launch_instance_id+'''<li>
			<li> IP Address: '''+pub_ip+'''<li>
		</ul>
		<li> Open Remote Desktop Application </li>
		<li> Enter the IP column with the following IP address: '''+pub_ip+'''<li>
		<li> Log in as : <strong>Administrator</strong> <li>
		<li> The password for Administrator is : '''+passwd+'''<li>
		<li> It is recommended that you change your password for security purposes<li>
	</ul>
</body>
</html>'''

print web







