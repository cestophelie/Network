import os
import socket

host = '192.168.21.132'
port = 10080
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen(5)

# connectionSocket, addr = serverSocket.accept()


while True:
	connectionSocket, addr = serverSocket.accept()
	print("Connection from: " + str(addr))
	req = connectionSocket.recv(1024)  # get the request, 1kB max
	reqStr = req.decode() # bytes to string
	reqStr = reqStr.split()[1]
	print('reqStr : '+reqStr)
	reqStr.lstrip()
	reqStr = reqStr.split('/')
	reqStr = reqStr[1]
	print('This is request: ' + str(reqStr))
	
	
	# print(type(req))
        # 1. Image type checking
	# 2. Non persistent mode
	

	filename = reqStr

	try:
		if 'html' in filename:
			f = open(filename, 'r')
			connectionSocket.sendall(str.encode("HTTP/1.0 200 OK\n",'iso-8859-1'))
			connectionSocket.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
			connectionSocket.send(str.encode('\r\n'))

		# send data per line
			for l in f.readlines():
				print('Sent ', repr(l))
				connectionSocket.sendall(str.encode(""+l+"", 'iso-8859-1'))
				l = f.read(1024)
			f.close()
		else:
			f1 = open(filename, 'rb')
			connectionSocket.sendall(str.encode("HTTP/1.0 200 OK\n"))
			connectionSocket.sendall(str.encode('Content-Type : image/jpg\n'))
			connectionSocket.sendall(str.encode('\r\n'))
			byte = f1.read(1024)
			connectionSocket.sendall(byte)
			while byte:
				byte = f1.read(1024)
				connectionSocket.sendall(byte)
			f1.close()
	except FileNotFoundError:
		# path = str("'./") + filename + str("'")
		# if os.path.isfile(path):
		f2 = open('notFound.html','r')
		connectionSocket.sendall(str.encode("HTTP/1.0 200 OK\n",'iso-8859-1'))
		connectionSocket.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
		connectionSocket.send(str.encode('\r\n'))
		for l in f2.readlines():
			print('Sent ', repr(l))
			connectionSocket.sendall(str.encode(""+l+"", 'iso-8859-1'))
			l = f2.read(1024)
		f2.close()	
		#print('else case')
		#break
	'''byte = f.read(1024)
	while byte:
		byte = f.read(1024)
		connectionSocket.sendall(byte.encode('utf-8'))'''
		
	# msg = 'sewoni jjang'
	#connectionSocket.send(str.encode(msg))
	connectionSocket.close() # persistent?

# connectionSocket.close()
