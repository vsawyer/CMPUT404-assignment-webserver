# coding: utf-8
import SocketServer
import os
import mimetypes
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# Copyright 2015 Valerie Sawyer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    statusLine = ""
    def handle(self):
        self.data = self.request.recv(1024).strip()     
        totalRequest = self.data.splitlines()
        requestLine = totalRequest[0].split()
        if requestLine[1].endswith("/"):
            path = os.path.abspath("www" + requestLine[1] + "index.html")
        elif requestLine[1].endswith("p"):
            path = os.path.abspath("www" + requestLine[1] + "/index.html")
        else:
            path = os.path.abspath("www" + requestLine[1])
        if os.path.isfile(path) and os.path.abspath("www") in os.path.realpath(path):
            mimetype, _ = mimetypes.guess_type(path) 
            contentType = "Content-Type: " + mimetype + "\r\n\n"
            try:
                file = open(path, 'r')
            except IOError:
                statusLine = "HTTP/1.1 404 Not Found"
                self.request.sendall(statusLine)  
            statusLine = "HTTP/1.1 200 OK\r\n"
            self.request.sendall(statusLine + contentType + file.read())
            file.close()
        else:
            statusLine = "HTTP/1.1 404 Not Found"
            self.request.sendall(statusLine)
            
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
