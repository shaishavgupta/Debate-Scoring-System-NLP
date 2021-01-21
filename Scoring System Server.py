import socket
import sys
import time
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer 

#BINDING SERVER
print("welcome to chat system")
print("")
print("Initializing.....")
time.sleep(1)
s=socket.socket()
host=socket.gethostname()
print("serve will start soon....")
port=8085
print("host name is :",host)
s.bind((host,port))
print("")
print("server is waiting for incoming connection")
s.listen(2)


#CONNECTION INTIALIZATION MESSAGE FUNCTION
def connection(conn,addr):
	   
	   print("address is :",addr)
	   print("client one has connected")
	   conn.send("welcome to MY CHAT".encode())
	   print(addr," Your Topic is Internet a boon or bane")


#ACCEPTING CONNECTION FOR CLIENT1 & CLIENT2
conn1,addr1=s.accept()
connection(conn1,addr1)
conn2,addr2=s.accept()
connection(conn2,addr2)

#SAVING NAMES
c1_name=conn1.recv(1024)
c1_name=c1_name.decode()
print(c1_name,"Has connected to chat system")

# c1_name=conn1.recv(1024)
# c1_name=c1_name.decode()
# print(c1_name,"Your Topic is Internet a boon or bane")

c2_name=conn2.recv(1024)
c2_name=c2_name.decode()
print(c2_name,"Has connected to chat system")

conn1.send(c2_name.encode())
conn2.send(c1_name.encode())

message="Let's start the  game, message should be sent 1 by 1"
conn1.send(message.encode())
conn2.send(message.encode())
print("message sent....")
####################################

#creating stop words
stop_words = stopwords.words('english')
stop_words.append('us')
#reading files
for_the_motion = open("for_the_motion.txt",'r')
against_the_motion = open("against_the_motion.txt",'r')

#file type casting
fors = for_the_motion.read()
for_the_motion.seek(0)
against = against_the_motion.read()
against_the_motion.seek(0)


#tokenizing the data

#initialising  for the motion
lst_for = []
lst_for = word_tokenize(fors)

fors = []

for i in range(len(lst_for)):
	if (lst_for[i].isalpha() and not(lst_for[i].lower() in stop_words) and not(lst_for[i] in fors)):
		fors.append(lst_for[i])


lst_for = set()
for i in fors:
	if not(i in lst_for):
		for syn in wordnet.synsets(i):
			for l in syn.lemmas():
				lst_for.add(l.name())
		
#initialising against the motion
lst_against = []
lst_against = word_tokenize(against)
against = []


for i in range(len(lst_against)):
	if (lst_against[i].isalpha() and not(lst_against[i].lower() in stop_words) and not(lst_against[i] in against)):
		against.append(lst_against[i])
		
lst_against = set()
for i in against:
	if not(i in lst_against):
		for syn in wordnet.synsets(i):
			for l in syn.lemmas():
				lst_against.add(l.name())  

#assigning player keywords and scores
player1 = set()
player2 = set()
player1_score = 0
player2_score = 0

####################################

#CHAT LOOP
loop=0
while 1:
		
	if(loop>3):
		break
	loop+=1

	def filter_out(string,player):
		if(len(string)==0 or string==None):
			return [0,0]

		ps = PorterStemmer() 

		player1_score = 0
		player2_score = 0
		#tokenisation
		lst = []
		statement = []
		statement = word_tokenize(string)

		#removing stop words and characters
		for i in range(len(statement)):
			if (statement[i].isalpha() and not(statement[i].lower() in stop_words)):
				lst.append(statement[i])

		#finding synonyms
		if(player==1):
			synonyms = []

			for i in lst:
				if not(i in player1) and ((i in lst_for) or (ps.stem(i) in lst_for)):
					player1_score+=1
					synonyms.append(i)
					for syn in wordnet.synsets(i):
						for l in syn.lemmas():
							synonyms.append(l.name())
							
				elif (not(i in player1) and not(i in lst_for)):
					flag = 0
					tmp = []
					for syn in wordnet.synsets(i):
						for l in syn.lemmas():
							tmp.append(l.name())
					
					flag=1
					for k in tmp:
						if not(k in player1) and ((k in lst_for) or (ps.stem(k) in lst_for)):
							if flag:
								player1_score+=1
								synonyms.append(k)
								synonyms.append(ps.stem(k))
								for syn in wordnet.synsets(k):
									for l in syn.lemmas():
										synonyms.append(l.name())
								flag=0
							
				
			for i in synonyms:
				player1.add(i)
		else:
			synonyms = []

			for i in lst:
				if (not(i in player2)) and ((i in lst_against) or (ps.stem(i) in lst_against)):
					synonyms.append(i)

					player2_score+=1
					for syn in wordnet.synsets(i):
						for l in syn.lemmas():
							synonyms.append(l.name())
							
				elif (not(i in player2) and not(i in lst_against)):
					tmp = []
					for syn in wordnet.synsets(i):
						for l in syn.lemmas():
							tmp.append(l.name())
					
					flag=1
					for k in tmp:
						if not(k in player2) and ((k in lst_against) or (ps.stem(k) in lst_against)):
							if flag:
								player2_score+=1
								synonyms.append(k)
								synonyms.append(ps.stem(k))
								for syn in wordnet.synsets(k):
									for l in syn.lemmas():
										synonyms.append(l.name())
								flag=0
				
			for i in synonyms:
				player2.add(i)
				
		#clearing
		synonyms.clear()
		lst.clear()
		scores = []
		scores.append(player1_score)
		scores.append(player2_score)
		return scores

	c1_message=conn1.recv(1024)
	print(c1_name,":",c1_message.decode())
	conn2.send(c1_message)

	m = filter_out(c1_message.decode(),1)
	player1_score = player1_score+m[0]
	player2_score = player2_score+m[1]


	c2_message=conn2.recv(1024)
	print(c2_name,":",c2_message.decode())
	conn1.send(c2_message)
	m = filter_out(c2_message.decode(),2)
	player1_score = player1_score+m[0]
	player2_score = player2_score+m[1]


	concat = str(player1_score)+" "+str(player2_score)

	conn1.send(concat.encode())
	conn2.send(concat.encode())
	
	

if(player1_score>player2_score):
	x = c1_name," wins by ",player1_score-player2_score," points"

elif(player2_score>player1_score):
	x = c2_name," wins by ",player2_score-player1_score," points"

else:
	x = " same points match draw"

out = ""
for i in x:
	out += str(i)

conn1.send(out.encode())
conn2.send(out.encode())