#!/usr/bin/python2
import cgi,commands,time,mysql.connector,json

print "content-type:text/html"
print ""

data=cgi.FieldStorage()
uname=data.getvalue('uname')
sg=data.getvalue('sg')
sec_id=data.getvalue('exsg')
ami=data.getvalue('os')
iam=data.getvalue('iam')
cnt=data.getvalue('cnt')
rules=data.getvalue('option')

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="abhi",
	database="aws"  
)

mycursor = mydb.cursor()


key_pair="project1"
key_pair_path="/root/Downloads/project1.pem"



ami_id="gggggg"

def sg_rules():
	commands.getoutput('sudo aws ec2 authorize-security-group-ingress --group-name '+sg+' --protocol tcp --port 22 --cidr 0.0.0.0/0')
	if(rules=="yes"):
		ports=data.getvalue('ports')
		for port in ports:
			commands.getoutput('sudo aws ec2 authorize-security-group-ingress --group-name '+sg+' --protocol tcp --port '+port+' --cidr 0.0.0.0/0')



	
	

# selecting ami-id and creating inbound rules for security group -----

if ami=="a":
	ami_id="ami-5b673c34"
elif ami=="b":
	ami_id="ami-efd0428f"
else:
	ami_id="ami-c2c3a2a2"

# attaching an iam role to the ec2 instance


def attach_iam(instance_id,role):
	commands.getoutput('sudo aws iam create-instance-profile --instance-profile-name '+uname)
	commands.getoutput('sudo aws iam add-role-to-instance-profile --role-name '+role+' --instance-profile-name '+uname)
	commands.getoutput('sudo aws ec2 associate-iam-instance-profile --instance-id '+instance_id+'  --iam-instance-profile Name='+uname)
	


if sg is not None:
	sec_id=commands.getoutput('sudo aws ec2 create-security-group --group-name '+sg+' --description "security group for development environment in EC2" --query "GroupId"')
	sg_rules()
	
	
	

# launching instance ---

launch_instance_id=commands.getoutput('sudo aws ec2 run-instances --image-id '+ami_id+' --security-group-ids '+sec_id+' --count '+cnt+' --instance-type t2.micro --key-name '+key_pair+' --query "Instances[0].InstanceId"')







# GET THE PASSWORD FOR WINDOWS INSTANCE ---

win_passwd="aaa"

if ami_id=="ami-c2c3a2a2":
	win_passwd=commands.getoutput('sudo aws ec2 get-password-data --instance-id  '+launch_instance_id+' --priv-launch-key '+key_pair_path+' --query "PasswordData"')

time.sleep(10)

if iam=="bb":
	iam="ec2s3full"
	attach_iam(launch_instance_id.strip(""),iam)
elif iam=="cc":
	iam="ec2s3ro"
	attach_iam(launch_instance_id.strip(""),iam)


# Fetching public ip of instance ----

pub_ip=commands.getoutput('sudo aws ec2 describe-instances --instance-ids '+launch_instance_id+' --query "Reservations[0].Instances[0].PublicIpAddress"')


# ADDING ENTRY OF EC2 INSTANCE AND SECURITY GROUP IN DATABASE
if sg is not None:
	sql = "INSERT INTO ec2 (name, instance_id,security_group) VALUES (%s, %s, %s)"
	val = (uname, launch_instance_id,sec_id)
	mycursor.execute(sql, val)
	mydb.commit()





# Script to be downloaded by client ----

web='''
<!Doctype html>
<html>
<head>
	<title>yoyoyoy</title>
</head>
<body style="background-color:powderblue;">
	<h1> We have successfully processed your request</h1>
	<br>
	<p> Just follow the instructions to access to your instance </p>
	<p> Please note down the following details related to your instance </p>
	<ul> For Linux Instances
		<li>Instance Id-- '''+launch_instance_id+'''</li>
		<li>Public IP -- '''+pub_ip+'''</li>
		<li><a href="/mykey.pem" download > Download this </a> file ,to get the access key-pair file</li>
		<li>To access instance, give the full path of the file you downloaded</li>
	</ul>
	<p> Your IAM ROLE ATTACHED TO THE INSTANCE IS : '''+create_profile+'''</p>
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
		<li> The password for Administrator is : '''+win_passwd+'''<li>
		<li> It is recommended that you change your password for security purposes<li>
	</ul>
</body>
</html>'''

print web











