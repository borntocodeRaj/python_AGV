#!/usr/bin/python

import sys
import threading
import os
from time import sleep
lock = threading.Lock();


ip_list = []

class Thread1( threading.Thread):
	def __init__(self,addr): 
		super(Thread1, self).__init__()
		self.addr=addr
		self.cmd="ping -c 2 -w 2 "+addr+" 1>/dev/null 2>/dev/null"

	def run(self):
                global ip_list
		if os.system(self.cmd)==0:
			with lock:
                                ip_list.append(self.addr)


if len(sys.argv)!=2:
	print "One parameter please, as 192.168.37."
else:
        print "Ping Test:"
        threads=[]
	for i in range(1,255):
		addr=sys.argv[1]+str(i)
		th=Thread1(addr)
		th.start()
                threads.append(th)
        for th in threads:
                th.join()
        print ip_list
