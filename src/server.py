#/* encoding=utf-8 */

################################################################################
##  Feature  : HTTP server.
##  Author   : zhanglue
##  Date     : 2019.01.24
################################################################################

import sys
import socket

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import urlparse

from shell import make_dir
from log import TheLogger

def is_port_idle(port):
    """
    Return if port is idle.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = get_host_ip()
    try:
        s.connect((ip, port))
        s.shutdown(2)
        return False
    except:
        return True

    return False


class RequestHandler(BaseHTTPRequestHandler):
    """
    Request handler of HTTP server.
    """
    def log_message(self, f, *args):
        """
        Forbidden logging.
        """
        TheLogger.debug(f % args)

    def do_GET(self):
        """
        Process GET requests.
        """
        self.send_response(200)
        for k, v in dict(self.headers).items():
            self.send_header(str(k), str(v))
        self.send_header('Content-Length', len("AAAA".encode()))
        self.end_headers()
        self.wfile.write("AAAA".encode())

    def do_POST(self):
        """
        Process POST requests.
        """
        return


class HttpServer():
    """
    HTTP server.
    """
    def __init__(self, ip, port):
        """
        Initialize.
        """
        self.ip = ip
        self.port = port

    def start(self):
        """
        Start server.
        """
        server = HTTPServer((self.ip, self.port), RequestHandler)
        server.serve_forever()


if __name__ == '__main__':
    """
    Main enter.
    """
    serverHost = sys.argv[1]
    try:
        serverPort = int(sys.argv[2])
    except Exception as e:
        print("Error: specify port correctly.")
    pathLog = sys.argv[3]

    make_dir(pathLog, force = True)
    TheLogger.init(pathLog, "server.log", forbiddenStd=True)

    if not serverHost or not serverPort:
        TheLogger.error('Set server host and port.')
        exit(1)

    TheLogger.info('Start HTTP server with %s:%s...' % (serverHost, serverPort))
    httpServer = HttpServer(serverHost, serverPort)
    httpServer.start()

