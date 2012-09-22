#!/usr/bin/python
import SimpleHTTPServer
import SocketServer
import logging
import cgi

PORT = 8000

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        print self.headers
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
	print '{} --> {}'.format(self.client_address,  self.rfile.read(int(self.headers["Content-Length"])))
	self.send_response(200)
	self.end_headers()

Handler = ServerHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)
print "serving at port", PORT
httpd.serve_forever()
