import sys
# from time import sleep
import time
import socket
from packet import pkt
import threading

serverPort = 10080
idList = ''
userIP = []
timeout = []
delHaltFlag = 1
ipTable = ''

def sendInfo(server):
    req = 1
    msg = b''
    externalIP = ''
    global idList
    global userIP
    global ipTable
    for i in range(len(userIP)):
        userID = str(userIP[i]).encode()
        sendPkt = pkt()
        sendPkt = sendPkt.setPacketInfo(req, userID, msg, idList.encode(), externalIP.encode(), ipTable.encode())
        server.sendto(sendPkt, userIP[i]) 


def timeoutCheck(server):
    global timeout
    global idList
    global userIP
    global delHaltFlag

    while True:
        if delHaltFlag != 0:
            length = len(timeout)
            for i in range(0, length):
                currentTime = time.time()
                if currentTime - timeout[i][2] > 30:
                    print(timeout[i][0] + ' is disappeared '+str(timeout[i][1]))
                    delID = timeout[i][0] + ' ' + str(timeout[i][1]) + '*'
                    idList = idList.replace(delID, '')
                    delIdx = userIP.index(timeout[i][1])
                    del userIP[delIdx]
                    del timeout[i]
                    sendInfo(server)
                    break
                
            time.sleep(0.97)


def server():
    ip = ''
    global serverPort
    global idList
    global userIP
    global timeout
    global delHaltFlag
    global ipTable

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((ip, serverPort))

    thread = threading.Thread(target = timeoutCheck, args = (server,))
    thread.daemon = True
    thread.start()
    
    while True:
        recv, clientAddr = server.recvfrom(2048)
        received = pkt()
        received.readPacket(recv)
        
        if received.req == 0:
            print(str(received.userID.decode()) + ' ' + str(clientAddr))
            user = received.userID.decode().rstrip('\x00')
        
            idList = idList + user + ' ' + str(clientAddr) + '*'
            
            external = received.externalIP.decode().rstrip('\x00')
            privateIP = (external, 10081)
            if str(clientAddr[0]) != str(external):
                ipTable = ipTable + str(clientAddr) + ' ' + str(privateIP) + '*'

            userIP.append(clientAddr)
            timeout.append([user, clientAddr, time.time()])

            sendInfo(server)

        elif received.req == 1:
            delHaltFlag = 0
            user = received.userID.decode().rstrip('\x00')
            print(user + ' is unregistered' + ' ' + str(clientAddr))
            delID = user + ' ' + str(clientAddr) + '*'
            idList = idList.replace(delID, '')
            delIdx = userIP.index(clientAddr)
            del userIP[delIdx]
            for i in range(len(timeout)):
                if timeout[i][0] == user:
                    del timeout[i]
                    break

            sendInfo(server)
            delHaltFlag = 1

        else:
            # keep alive part
            for i in range(len(timeout)):
                if str(timeout[i][1]) == str(clientAddr):
                    timeout[i][2] = time.time()  # last in time update
            
    pass

"""
Don't touch the code below
"""
if  __name__ == '__main__':
    server()
