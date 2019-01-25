#/* encoding=utf-8 */

################################################################################
##  Feature  : HTTP server.
##  Author   : zhanglue
##  Date     : 2019.01.24
################################################################################

import os
import sys
import socket
from collections import defaultdict
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import urlparse

from json_api import json_dumps
from json_api import json_file_to_pyData
from json_api import pyData_to_json_file
from log import TheLogger
from utility import get_env_var
from utility import is_port_idle
from utility import make_dir
from utility import path_join

from os.path import dirname
from os.path import abspath
from os.path import expanduser
__pathCur = dirname(abspath(expanduser(__file__)))
PATH_ROOT = abspath(os.path.join(__pathCur, "../"))

class RequestHandler(BaseHTTPRequestHandler):
    """
    Request handler of HTTP server.
    """
    def log_message(self, f, *args):
        """
        Forbidden logging.
        """
        TheLogger.debug("INNER: " + f % args)

    def response_OK(self, respMsg = "OK\n"):
        """
        Reponse "OK".
        """
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-Length", len(respMsg.encode()))
        self.end_headers()
        self.wfile.write(respMsg.encode().encode())

    def response_404(self, respMsg = "Url not found.\n"):
        """
        Response 404.
        """
        self.send_response(404)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-Length", len(respMsg))
        self.end_headers()
        self.wfile.write(respMsg.encode())

    def response_500(self, respMsg = "FAILED\n"):
        """
        Response 500.
        """
        self.send_response(500)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-Length", len(respMsg))
        self.end_headers()
        self.wfile.write(respMsg.encode())

    def do_GET(self):
        """
        Process GET requests.
        """
        urlEntire = "http://" + self.client_address[0] + self.path
        urlPieces = urlparse(urlEntire)
        urlPath = urlPieces.path.strip("/")
        urlQueries = {}
        if urlPieces.query:
            urlQueries = dict(
                    [x.split("=",1) for x in urlPieces.query.split("&")])

        TheLogger.info("Recieved request: %s" % urlEntire)
        TheLogger.debug("Recieved request's urlpath : %s" % urlPath)
        TheLogger.debug("Recieved request's queries : %s" % urlQueries)

        if not urlPath:
            self.response_OK()
            return

        responsePattern = get_response_pattern()
        responsePattern = defaultdict(lambda: None, responsePattern)
        pattern = responsePattern[urlPath]
        if not pattern:
            self.response_404()
            return

        self.send_response(200)
        headersNormal = {
                "Content-Length": len(pattern["respData"]),
                "Content-type": "text/plain"
                }
        headersExt = {}
        if "headers" in pattern:
            headersExt = pattern["headers"]
        headers = {**headersNormal, **headersExt}
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(pattern["respData"].encode())

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
        TheLogger.error("Set server host and port.")
        exit(10)

    if not is_port_idle(serverPort):
        TheLogger.error("Port {} is in use.".format(serverPort))
        exit(11)

    TheLogger.info("Start HTTP server with %s:%s..." % (serverHost, serverPort))
    httpServer = HttpServer(serverHost, serverPort)
    httpServer.start()


def get_response_pattern():
    """
    Get response data.
    """
    responsePattern = {}
    try:
        responsePattern = json_file_to_pyData(pathRespPatternFile)
        if not responsePattern:
            responsePattern = {}
        TheLogger.debug("Current response pattern: \n" + \
                json_dumps(responsePattern))
    except Exception as e:
        TheLogger.error(str(e))

    return responsePattern


def set_response_pattern(pathRespPatternFileIn, flagAddData):
    """
    Set response data.
    """
    try:
        responsePatternIn = json_file_to_pyData(pathRespPatternFileIn)
        TheLogger.debug("Input response pattern: \n" + \
                json_dumps(responsePatternIn))

        responsePatternOrg = {}
        if flagAddData:
            responsePatternOrg = get_response_pattern()

        responsePattern = {**responsePatternOrg, **responsePatternIn}
        TheLogger.debug("Incomming response pattern: \n" + \
                json_dumps(responsePattern))

        pyData_to_json_file(responsePattern, pathRespPatternFile)
    except Exception as e:
        TheLogger.error(str(e))


if __name__ == "__main__":
    """
    Main enter.
    """
    pathTempDataDir = path_join(PATH_ROOT, "temp")
    pathRespPatternFile = path_join(pathTempDataDir, "response_pattern.json")
    make_dir(pathTempDataDir)
    TheLogger.init(pathTempDataDir, "server.log")

    mode = sys.argv[1]
    if mode == "start":
        serverHost = "127.0.0.1"
        try:
            serverPort = int(sys.argv[2])
        except Exception as e:
            print("Error: specify port correctly.")
        start(serverHost, serverPort)
    elif mode == "set_response_pattern":
        pathRespPatternFileIn = sys.argv[2]
        flagAddData = bool(int(sys.argv[3]))
        set_response_pattern(pathRespPatternFileIn, flagAddData)
    elif mode == "get_response_pattern":
        get_response_pattern()
    else:
        TheLogger.error("Unknown parameter {}.".format(mode)) 

