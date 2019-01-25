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

from utility import get_env_var
from utility import is_port_idle
from utility import make_dir
from log import TheLogger

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


def start(serverHost, serverPort):
    """
    Start HTTP server.
    """
    if not serverHost or not serverPort:
        TheLogger.error('Set server host and port.')
        exit(10)

    if not is_port_idle(serverPort):
        TheLogger.error("Port {} is in use.".format(serverPort))
        exit(11)

    TheLogger.info('Start HTTP server with %s:%s...' % (serverHost, serverPort))
    httpServer = HttpServer(serverHost, serverPort)
    httpServer.start()


def set_data(pathDataFile, flagAddData):
    """
    Set behaviour/data.
    """
    TheLogger.info(pathDataFile)
    TheLogger.info(str(flagAddData))


if __name__ == '__main__':
    """
    Main enter.
    """
    pathTempDataDir = sys.argv[1]
    make_dir(pathTempDataDir)
    TheLogger.init(pathTempDataDir, "server.log")

    mode = sys.argv[2]
    if mode == "start":
        serverHost = "127.0.0.1"
        try:
            serverPort = int(sys.argv[3])
        except Exception as e:
            print("Error: specify port correctly.")
        start(serverHost, serverPort)
    elif mode == "set":
        pathDataFile = sys.argv[3]
        flagAddData = bool(int(sys.argv[4]))
        set_data(pathDataFile, flagAddData)
    else:
        TheLogger.error("Unknown parameter {}.".format(mode)) 

