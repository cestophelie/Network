from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)
print('The TCP server is ready to receive')

connectionSocket, addr = serverSocket.accept()
while True:
	# connectionSocket, addr = serverSocket.accept()
	print('addr : '+str(addr))
	msg = connectionSocket.recv(1024).decode()
	newMsg = msg.upper()
	connectionSocket.send(newMsg.encode())
	
connectionSocket.close()
