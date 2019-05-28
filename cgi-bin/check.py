#!/usr/bin/python2
import cgi,commands
print "content-type:text/html"
print ""
data=cgi.FieldStorage()
user=data.getvalue('username')
password=data.getvalue('password')

ip = commands.getoutput('sudo myip')

if user=='manka' and password=='hello':
	
	print '<meta http-equiv="refresh" content="2; url=/redirect1.html" />'
else:
	print "invalid Entry..!! We will be redirecting you to the login page"
	print "<script>setTimeout(\"location.href='/index.html';\",5000);</script>"
