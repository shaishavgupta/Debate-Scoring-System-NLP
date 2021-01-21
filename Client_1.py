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
c1_name=input(str("Please enter your name:"))
port=8085
print("trying to connect..")
time.sleep(1)
s.connect((host,port))
print("connected")
message=s.recv(1024)
print("server sends :",message)


### connection done till here,Now after that username code ### #
s.send(c1_name.encode())
c2_name=s.recv(1024)
c2_name=c2_name.decode()
print("")
print(c2_name,"has joined the chat room")
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

    new_message=input("%s:"%c1_name)
    new_message=new_message.encode()
    s.send(new_message)
    message=s.recv(1024)
    message=message.decode()
    print(c2_name,":",message)
    message=s.recv(1024)
    message=message.decode()
    print(message)     

message=message.decode()
print(message)