import os
import socket
import time

def fileHtml(filename,connectionSocket):
	connectionSocket.sendall(str.encode("HTTP/1.1 200 OK\n",'iso-8859-1'))
	connectionSocket.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
	connectionSocket.sendall(str.encode('\r\n'))

	for i in filename.readlines():
		connectionSocket.sendall(str.encode(""+i+"", 'iso-8859-1'))
		i = filename.read(1024)
	# filename.close()


def fileImages(filename, connectionSocket):
	connectionSocket.sendall(str.encode("HTTP/1.1 200 OK\n"))
	connectionSocket.sendall(str.encode('Content-Type : image/jpg\n'))
	connectionSocket.sendall(str.encode('\r\n'))
	byte = filename.read(1024)
	connectionSocket.sendall(byte)
	while byte:
		byte = filename.read(1024)
		connectionSocket.sendall(byte)
	# filename.close()


def transfer(filename, csocket):
	if 'html' in filename:
		f = open(filename, 'r')
		fileHtml(f, csocket)
		f.close()
	else:
		f1 = open(filename, 'rb')
		fileImages(f1, csocket)
		f1.close()


port = 10080
startTime = 0
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 0))
host = s.getsockname()[0] # external ip address

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# serverSocket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSocket.bind((host,port))
serverSocket.listen(10) # -------

connectionSocket, addr = serverSocket.accept()
f = open('login.html', 'r')
fileHtml(f,connectionSocket)
f.close()

while True:
	connectionSocket, addr = serverSocket.accept()
	req = connectionSocket.recv(1024)
	req = req.decode()
	print(str(req))
	print('ADDRESS : '+str(addr))
	
	reqStr = req.split()[1]
	reqStr = reqStr.split('/')
	print('here : ' + str(req.split()[0]))
	reqStr = reqStr[1]
	
	#print('LOGIN : '+str(loginId))
	if (req.split()[0] == 'POST'):
		loginId = req.split()[-1]
		loginId = loginId.split('=')[1]
		loginId = loginId.split('&')[0]
		connectionSocket.sendall(str.encode("HTTP/1.1 200 OK\n",'iso-8859-1'))
		connectionSocket.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
		connectionSocket.sendall(str.encode('Set-Cookie: id='+loginId+'; Max-Age = 30;', 'iso-8859-1'))
		startTime = time.time()
		connectionSocket.sendall(str.encode('\r\n'))
		f = open('secret.html', 'r')
		for i in f.readlines():
			connectionSocket.sendall(str.encode(""+i+"", 'iso-8859-1'))
			i = f.read(1024)
		f.close()
		
		while True:
			csocket, caddr = serverSocket.accept()
			req1 = csocket.recv(1024)
			req1 = req1.decode()
			reqStr1 = req1.split()[1]
			reqStr1 = reqStr1.split('/')
			reqStr1 = reqStr1[1]
			print('CAddr : ' + str(caddr))
			print('Inner request : \n'+ str(req1))
			print(str(reqStr1))	
			if 'Cookie' in str(req1):
				filename = reqStr1
				print(filename)
				if filename=='cookie.html':
					csocket.sendall(str.encode("HTTP/1.1 200 OK\n",'iso-8859-1'))
					csocket.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
					csocket.sendall(str.encode("\r\n"))
					csocket.sendall(('<html><body>Hello '+str(loginId)+'<br>'+str(30-int(time.time()-startTime))+' seconds left until your cookie expires.</body></html>').encode())
				elif not str(reqStr1):
					f = open('login.html','r')
					fileHtml(f, csocket)
					# cookie restart
					f.close()
					break
				else:
					if not os.path.isfile(filename):
						print('yay')
						csocket.sendall(str.encode("HTTP/1.1 404 Not Found\n",'iso-8859-1'))
						csocket.sendall(str.encode("Content-type: text/html\n", 'iso-8859-1'))
						csocket.sendall(str.encode('\r\n'))
						
					else:
						transfer(filename, csocket)
			else:
				if not str(reqStr1):
					f = open('login.html','r')
					fileHtml(f, csocket)
					f.close()
					break
				else:
					csocket.sendall(str.encode("HTTP/1.1 403 Forbidden\n", 'iso-8859-1'))
					csocket.sendall(str.encode("Content-type: text/html\n", 'iso-8859-1'))
					csocket.sendall(str.encode("\r\n"))
				# break
			csocket.close()
			continue
	elif not str(reqStr):
		f = open('login.html','r')
		fileHtml(f, connectionSocket)
		f.close()
	
	else:
		connectionSocket.sendall(str.encode("HTTP/1.1 403 Forbidden\n", 'iso-8859-1'))
		connectionSocket.sendall(str.encode("Content-type: text/html\n", 'iso-8859-1'))
		connectionSocket.sendall(str.encode("\r\n"))


	connectionSocket.close()

connectionSocket.close()
