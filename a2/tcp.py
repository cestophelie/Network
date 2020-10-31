from socket import *
serverIP = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverIP,serverPort))

while True:
	msg = input('Input lowercase sentence : ')
	clientSocket.send(msg.encode())

	newMsg = clientSocket.recv(1024)
	print('From server : ',newMsg.decode())

clientSocket.close()
