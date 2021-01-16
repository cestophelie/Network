# can test with various types of file extensions since all files are binary

import time
import threading

programStart = round(time.time(),2)
logTxt = open("log.txt","w")#comes after the time start point for the accurate measurement

def fileCopy(src, des):
        file1 = open(src,"rb")
        file2 = open(des, "wb")

        start = round(time.time(),2)
        logTxt.write(str(round(start - programStart,2))+"  Start copying  "+src+"  to  "+des+"\n")
        byte = file1.read(10000)
        file2.write(byte)
        while byte:
                byte = file1.read(10000)
                file2.write(byte)
        finish = round(time.time(),2)
        logTxt.write(str(round(finish - programStart,2))+"  "+des+"  is copied completely\n")

threads = []
while(True):
	a = input("Input the file name: ")
	if(a == "exit"):
		exit()

	b = input("Input the new name: ")
	thread = threading.Thread(target = fileCopy, args = (a,b))
	threads.append(thread)
	thread.start()
	print("\n\n")

for thread in threads:
	thread.join()
