#!/usr/bin/python2

import sys
import os
import SimpleHTTPServer
import SocketServer


class RadioServer(SocketServer.ThreadingTCPServer):
	allow_reuse_address = True
	
	def __init__(self,a,b):
		SocketServer.ThreadingTCPServer.__init__(self,a,b)
		self.mpc("stop")
		self.current = -1
		self.load()

	def load(self):	
		self.playlist = []
		f = open("../playlist.txt")
		self.playlist = f.readlines()
		f.close()	
		for i in range(len(self.playlist)): 
			self.playlist[i] = self.playlist[i].rstrip("\n")	

	def mpc(self,cmd):
		print("MPC: " + cmd)
		os.system("mpc " + cmd)
		
	def getItemUrl(self,no):
		item = self.playlist[no]
		url = item.split("^")[2]
		return url


class RadioRequest(SimpleHTTPServer.SimpleHTTPRequestHandler):

	def __init__(self,req,clientAddress,server):
		SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self,req,clientAddress,server)
		self.server = server
		
	def do_GET(self):
	
		try: cmd = self.path.split("/")
		except: cmd = ""
		
		if (cmd[1] == "list"):
			self.procList()
		elif (cmd[1] == "stop"):
			self.procStop()
			self.server.load()
		elif (cmd[1] == "play"):
			self.procPlay(cmd[2])
		elif (cmd[1] == "state"):
			self.procState()
		else:
			SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

	def resp(self,kontent):
		self.send_response(200)
		self.send_header("Content-type","application/json")
		self.send_header("Content-length",len(kontent))
		self.end_headers()
		self.wfile.write(kontent)
		
	def report(self,cmd,state):
		self.resp("{\"result\":\"" + cmd + "\",\"current\":\"" + str(state) + "\"}\n")
			
	def procList(self):
		r = "{"
		if (self.server.current > -1):	cmd = "playing"
		else: cmd = "stopped"
		r += "\"result\":\"" + cmd + "\",\"current\":\"" + str(self.server.current) + "\","
		r += "\"list\":{"
		n = 1
		for item in self.server.playlist:
			if n > 1: r += ","
			r += "\"" + str(n) + "\":{"
			x = item.split("^")
			r += "\"n\":\"" + x[0] + "\","
			r += "\"i\":\"" + x[1] + "\","
			r += "\"s\":\"" + x[2] + "\""
			r += "}"
			n += 1
		r += "}}\n"
		self.resp(r)
	
	def procStop(self):
		self.server.current = -1
		self.server.mpc("stop")		
		self.server.mpc("repeat off")
		self.report("stopped",-1)
		
	def procPlay(self,no):
		try:
			self.server.current = int(no)
			self.server.mpc("clear")
			self.server.mpc("repeat on")
			url = self.server.getItemUrl(self.server.current - 1)
			self.server.mpc("add " + url)
			self.server.mpc("play 1")
			self.report("playing",self.server.current)		
		except:
			self.server.current = -1
			self.report("failed",-1)		
	
	def procState(self):
		if self.server.current == -1: sta = "stopped"
		else: sta = "playing"
		self.report(sta,self.server.current)


if __name__ == "__main__":
	try:		
		
		try: port = int(sys.argv[1])
		except: port = 0
		if port < 80: port = 8888
		
		path = os.path.dirname(sys.argv[0])
		os.chdir(path + "/web")
		
		httpd = RadioServer(("0.0.0.0",port),RadioRequest)
		httpd.allow_reuse_address = True
		print("Webserver listening on port " + str(port))
		httpd.serve_forever()
		
	except KeyboardInterrupt:
		print(" interrupted")
		httpd.shutdown()
