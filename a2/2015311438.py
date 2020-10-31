from socket import *

serverPort = 10080
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(5)
serverSocket.connect(('www.google.com', 10080))
cmd = 'GET file:///home/sewon42/Network/a2/index.html HTTP/1.0\r\n\r\n'.encode()
addr = 'file:///home/sewon42/Network/a2/index.html'
# serverSocket.send(cmd)
while True:
	print("hey")
	serverSocket, addr = serverSocket.accept()
	serverSocket.send("HTTP/1.1 200 OK\n"
        	 +"Content-Type: text/html\n"
	         +"\n" # Important!
        	 +"<html><body>Hello World</body></html>\n");
serverSocket.close()
'''while True: # 수신받을 수 있는 루프
    data = mysock.recv(512) # 512는 버퍼의 크기
    if(len(data) < 1):
        break
    print(data.decode())
    #데이터가 외부에서 오기 때문에 출력 전에 반드시 복호화(decode)
mysock.close()
'''
# serverSocket.bind(('', serverPort))
# serverSocket.listen(5)
print('The TCP server is ready to receive')
'''while True:
        connectionSocket, addr = serverSocket.accept()
        msg = connectionSocket.recv(1024).decode()
        newMsg = msg.upper()
        connectionSocket.send(newMsg.encode())
        connectionSocket.close()
'''
