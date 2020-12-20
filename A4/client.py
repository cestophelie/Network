import sys
import socket
import time
from packet import pkt
import threading

serverIP = '10.0.0.3'
serverPort = 10080
clientPort = 10081
userList = []
userMapping = {}
privateTable = {}
privateID = []
myIP = ''

def registerInfo(client):
    # make a separate thread for this
    global userList
    global userMapping
    global privateTable
    global privateID
    global myIP
        
    while True:
        recv, addr = client.recvfrom(2048)
        if addr[0] == '10.0.0.3':
            regInfo = pkt()
            regInfo.readPacket(recv)
            myIP = regInfo.userID.decode().rstrip('\x00')

            userList = regInfo.idList.decode().rstrip('\x00')
            userList = userList.split('*')
            for i in range(len(userList)-1):
                tmp = []
                tmp = userList[i].split(' ')
                userMapping[tmp[0]] = tmp[1]+' '+tmp[2]  # mapping ID and (IP + PORT)

            privateID = regInfo.ipTable.decode().rstrip('\x00')
            privateID = privateID.split('*')
            
            for j in range(0, len(privateID)-1):
                temp = []
                temp = privateID[j].split(' ')
                natIP = temp[0] + ' ' +temp[1]
                prvIP = temp[2] + ' ' + temp[3]
                
                privateTable[natIP] = prvIP
                
        else:  # chatting
            chatMsg = pkt()
            chatMsg.readPacket(recv)
            chatID = chatMsg.userID.decode().rstrip('\x00')
            message = chatMsg.msg.decode().rstrip('\x00')
            print('From ' + chatID + ' [' + message + ' ]')
            # print('Received from : ' +str(addr))
        
def chatting(client, clientCmd):
    # sending chat message to the given id
    global myIP
    myIP = str(myIP)
    sendMsg = []
    netCheck = []
    sendMsg = clientCmd.split(' ')
   
    addr = userMapping[sendMsg[1]]  # getting addr via id

    addr = addr.lstrip('(')
    addr = addr.rstrip(')')
    myIP = myIP.lstrip('(')
    myIP = myIP.rstrip(')')

    addr = eval(addr)
    myIP = eval(myIP)
    
    sendPkt = pkt()
    userID = clientID
    req = 2  # 2 is the chat msg sending mode
    msg = ''
    for i in range(2, len(sendMsg)):
        msg = msg + ' ' + sendMsg[i]
    idList = ''
    externalIP = '' 
    ipTable = ''
    sendPkt = sendPkt.setPacketInfo(req, userID.encode(), msg.encode(), idList.encode(), externalIP.encode(), ipTable.encode())
    
    if myIP[0] != addr[0]:
        client.sendto(sendPkt, addr)
    else:
        newAddr = privateTable[str(addr)]
        newAddr = eval(newAddr)
        # print('Sending to : '+str(newAddr))
        client.sendto(sendPkt, newAddr)

def keepAlive(client):
    req = 3  # req flag 3 for keep alive function
    msg = ''
    idList = ''
    externalIP = ''
    ipTable = ''
    alivePkt = pkt()
    alivePkt = alivePkt.setPacketInfo(req, clientID.encode(), msg.encode(), idList.encode(), externalIP.encode(), ipTable.encode())
    while True:
        time.sleep(10)
        client.sendto(alivePkt, (serverIP, serverPort))


def client(serverIP, serverPort):
    ip = ''
    # port = clientPort  # client prot different on machines
    global clientPort
    global userList
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind((ip, 10081))
    # external ip finding
    external = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    external.connect(('8.8.8.8',0))
    host = external.getsockname()[0]
    external.close()

    serverAddr = (serverIP, serverPort)
    userID = str(clientID)
    req = 0  # first sent
    msg = ''
    idList = ''
    externalIP = host
    ipTable = ''
    
    sendPkt = pkt()
    sendPkt = sendPkt.setPacketInfo(req, userID.encode(), msg.encode(), idList.encode(), host.encode(), ipTable.encode())
    client.sendto(sendPkt, serverAddr)

    thread = threading.Thread(target = registerInfo, args = (client,))
    thread.daemon = True
    thread.start()

    thread2 = threading.Thread(target = keepAlive, args = (client, ))
    thread2.daemon = True
    thread2.start()

    while True:
        clientCmd = input("")
        if clientCmd == '@show_list':
            for i in range(len(userList)):
                print(userList[i])
        elif clientCmd == '@exit':
            # delete from ip and idList
            req = 1  # exit request
            msg = ''
            idList = ''
            externalIP = host
            ipTable = ''
            exitPkt = pkt()
            exitPkt = exitPkt.setPacketInfo(req, clientID.encode(), msg.encode(), idList.encode(), externalIP.encode(), ipTable.encode())
            client.sendto(exitPkt, serverAddr)
            exit(0)

        elif '@chat' in clientCmd:
            chatting(client, clientCmd)

    pass


"""
Don't touch the code below!
"""
if  __name__ == '__main__':
    clientID = input("Enter ID : ")
    print()
    client(serverIP, serverPort)

