import socket
import sys
import time


print("welcome to chat system")
print("")
print("Initializing.....")
time.sleep(1)
s=socket.socket()


#host=input("Please enter the Server Address:")
host=socket.gethostname()
c2_name=input(str("Please enter your name:"))
port=8085
print("trying to connect..")
time.sleep(1)
s.connect((host,port))
print("connected")
message=s.recv(1024)
print("server sends :",message)

### connection done till here,Now after that username code ### #
s.send(c2_name.encode())
c1_name=s.recv(1024)
c1_name=c1_name.decode()
print("")
print(c1_name,"has joined the chat room")
print("")
message=s.recv(1024)
message=message.decode()
print("server:",message)

loop=1
### username code done till here, now messaging code...###
while 1:
	if(loop>3):
		break
	loop+=1
	message=s.recv(1024)
	message=message.decode()
	print(c1_name,":",message)
	new_message=input("%s:"%c2_name)
	new_message=new_message.encode()
	s.send(new_message)
	message=s.recv(1024)
	message=message.decode()
	print(message)

message=message.decode()
print(message)