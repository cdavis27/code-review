import sys
import errno
import select
import socket
import sys
import traceback
import time
import re
import os
from email.utils import formatdate
from urlparse import urlparse
from config_parser import ParsedConfig

class Poller:
    """ Polling server """
    def __init__(self,port):
        self.host = ""
        self.port = port
        self.open_socket()
        self.clients = {}
        self.size = 1024
        self.timeouts = {}
        # self.timeout = 0
        self.cache = {}
        self.config = ParsedConfig()
        self.upper = 0
        self.lower = 0

    def open_socket(self):
        """ Setup the socket for incoming clients """
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            self.server.bind((self.host,self.port))
            self.server.listen(5)
            self.server.setblocking(0)
        except socket.error, (value,message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)

    def run(self):
        """ Use poll() to handle each incoming client."""
        
        self.poller = select.epoll()
        self.pollmask = select.EPOLLIN | select.EPOLLHUP | select.EPOLLERR
        self.poller.register(self.server,self.pollmask)
        self.timeout = float(self.config.parameters["timeout"])
        recentSweep = time.time()

        while True:
             # poll sockets
            try:
                fds = self.poller.poll(timeout=1)
            except:
                return
            for (fd,event) in fds:
                # handle errors
                if event & (select.POLLHUP | select.POLLERR):
                    self.handleError(fd)
                    continue
                # handle the server socket
                if fd == self.server.fileno():
                    self.handleServer()
                    continue
                # handle client socket
                result = self.handleClient(fd)
                # self.clients[fd]

             # kill cliesnts that are older than the most recent time sweep
            for client in self.timeouts:
                if(time.time() - self.timeouts[client]) > self.timeout:
                    recentSweep = time.time()
                    del self.timeouts[fd]
                    del self.clients[fd]
                    del self.cache[fd]
                    self.clients[fd].close

    def handleError(self,fd):
        self.poller.unregister(fd)
        if fd == self.server.fileno():
            # recreate server socket
            self.server.close()
            self.open_socket()
            self.poller.register(self.server,self.pollmask)
        else:
            # close the socket
            self.clients[fd].close()
            del self.clients[fd]
            # del self.timeouts[fd]

    def handleServer(self):
        # accept as many clients are possible
        while True:
            try:
                (client,address) = self.server.accept()
            except socket.error, (value,message):
                # if socket blocks because no clients are available,
                # then return
                if value == errno.EAGAIN or errno.EWOULDBLOCK:
                    return
                print traceback.format_exc()
                sys.exit()
            # set client socket to be non blocking
            client.setblocking(0)
            # self.timeouts[client.fileno()] = time.time()
            self.clients[client.fileno()] = client
            self.poller.register(client.fileno(),self.pollmask)

    def handleClient(self,fd):
        try:
            data = self.clients[fd].recv(self.size)
            self.timeouts[fd] = time.time()
        except socket.error, (value,message):
            # if no data is available, move on to another client
            if value == errno.EAGAIN or errno.EWOULDBLOCK:
                return
            print traceback.format_exc()
            sys.exit()

        if data:
            if "\r\n\r\n" in data:
                if fd in self.cache:
                    data = self.cache[fd] + data
                    del self.cache[fd]

                response = self.getResponse(data)
                self.clients[fd].send(response)
                self.timeouts[fd] = time.time()
                # self.clients[fd].send(file) file = url

            else:
                if not fd in self.cache:
                    self.cache[fd] = data

                else:
                    self.cache[fd] += data

        else:
            self.poller.unregister(fd)
            self.clients[fd].close()
            del self.clients[fd]
            del self.timeouts[fd]
            if fd in self.cache:
                del self.cache[fd]

    def getResponse(self, data):
        # parse request
        response = ""

        message = data.split("\r\n\t\n", 1)
        lines = message[0].split("\r\n")
        words = lines[0].split()
        method = words[0]
        url = urlparse(words[1])
        version = words[2]

        headers = {}
        for i in range(1, len(lines)):
            headerSplit  = lines[i].split(":", 1)
            if len(headerSplit) > 1:
                headers[headerSplit[0].strip().lower()] = headerSplit[1].strip()
        if "range" in headers:
            rangeHeader = headers["range"]
            bytes = map(int, re.findall('\d+', rangeHeader))
            self.lower = bytes[0]
            self.upper = bytes[1]

        # start building response
        host = headers["host"]
        code = ""
        filePath = ""

        if method != "GET" and method != "HEAD":
            code = "501"
        else:
            filePath = self.getFilePath(url, host)
            # print filePath
            try:
                open (filePath)
                if "range" in headers:
                    code = "206"
                else:
                    code = "200"
            except IOError as ( errno , strerror ):
                if errno == 13:
                    code = "403"
                elif errno == 2:
                    code = "404"
                else :
                    code = "500" 

        statusLine = self.getStatusLine(code)
        responseBody = self.getResponseBody(code, filePath)
        resHeaders = self.getHeaders(code, headers, responseBody, filePath, method)

        return self.toString(code, statusLine, responseBody, resHeaders, method)

    def getFilePath(self, url, host):
        path = url.path
        # print path

        if path.endswith(('/')):
            path += "index.html"

        if host in self.config.hosts:
            path = self.config.hosts[host] + path

        else:
            path = self.config.hosts["default"] + path

        return path
  
    def getStatusLine(self, code):
        statusLine = "HTTP/1.1 " + code

        if code == "200":
            statusLine += " OK"
            
        elif code == "400":
            statusLine += " BAD REQUEST"
            
        elif code == "403":
            statusLine += " FORBIDDEN"

        elif code == "404":
            statusLine += " NOT FOUND"
            
        elif code == "500":
            statusLine += " INTERNAL SERVER ERROR"
            
        elif code == "501":
            statusLine += " NOT IMPLEMENDTED"
            
        statusLine += "\r\nConnection: Keep-Alive\r\n"

        return statusLine

    def getResponseBody(self, code, filePath):
        responseBody = ""

        if code == "200":
            with open(filePath, "rb") as f:
                responseBody = f.read()

        elif code == "206":
            with open(filePath, "rb") as f:
                bytes = f.read()
                responseBody = bytes[self.lower: self.upper+1]

        elif code == "400":
            responseBody = "<html><body><h1>400 Bad Request</h1></body></html>"

        elif code == "403":
            responseBody = "<html><body>h1>403 Forbidden</h1></body></html>"

        elif code == "404":
            responseBody = "<html><body>h1>404 Not Found</h1></body></html>"

        elif code == "500":
            responseBody = "<html><body>h1>500 Internal Server Error</h1></body></html>"

        elif code == "501":
            responseBody = "<html><body>h1>501 Not Implemented</h1></body></html>"
  
        return responseBody

    def getHeaders(self, code, headers, responseBody, filePath, method):
        resHeaders = {}

        resHeaders["Date"] = formatdate(time.time(), localtime=False, usegmt=True)
        resHeaders["Server"] ="FBRD.02"

        if method != "HEAD":
            if code == "200" or code == "206":
                end = os.path.splitext(filePath)[1]
                resHeaders["Content-Type"] = self.config.medias[end[1:]]
                resHeaders["Last-Modified"] =  formatdate(os.stat(filePath).st_mtime, localtime=False, usegmt=True)
                resHeaders["Content-Length"] = str(os.path.getsize(filePath))

            else:
                resHeaders["Content-Type"] = self.config.medias["html"]
                resHeaders["Last-Modified"] = formatdate(time.time(), localtime=False, usegmt=True)
                resHeaders["Content-Length"] = str(len(responseBody))

        return resHeaders

    def toString(self, code, statusLine, responseBody, resHeaders, method):
        response = statusLine 
        headers = ""
        for key, value in resHeaders.iteritems():
            headers += key + ": " + value + "\r\n"
        # print headers
        headers += "\r\n"    
        response += headers
        if method != "HEAD":
            response += responseBody

        return response