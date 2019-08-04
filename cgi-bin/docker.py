#!/usr/bin/python2
import cgi,commands,random


print "content-type:text/html"
print ""


data=cgi.FieldStorage()
container=data.getvalue('paas')

# Launching Container From Docker Image ------
# 'paas' container already has shellinabox service and some prog-language packages installed in it

port = random.randint(10000,40000)

container_id=commands.getoutput('sudo docker run -itd -p '+str(port)+':4200 paas') 

container_ip=commands.getoutput('sudo docker exec '+container_id+' hostname -i')

commands.getoutput('sudo docker exec -itd '+container_id+' shellinaboxd -t')

commands.getoutput('sudo docker exec -itd '+container_id+' service shellinaboxd restart')

base_ip=commands.getoutput('sudo myipg')


if container=="1":
	u="pyuser"
	p="py123"
elif container=="2":
	u="rubyuser"
	p="ruby123"
elif container=="3":
	u="javauser"
	p="java123"
else:
	u="phpuser"
	p="php123"



web='''
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Docker At Your ServiceCLOUD</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="background-color:powderblue">
  <h1 style="color:red">IAAS CLOUD</h1>

    <a href="http://'''+base_ip+":"+str(port)+'''" target="_blank"> Click here</a>
		<p> Type username = '''+u+'''<p>
	  <p> Type password = '''+p+''' </p>
</body>
</html>
'''
print web


