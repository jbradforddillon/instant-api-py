#!/usr/bin/python

import string
import json
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from argparse import ArgumentParser


parser = ArgumentParser(description='Process some integers.')
parser.add_argument("-f", "--file", dest="filename",
                    help="JSON file to serve", metavar="FILE")
parser.add_argument("-p", "--port", dest="port",
                    help="Port to listen on", metavar="PORT")

args = parser.parse_args().__dict__

file_arg = args['filename'] or "source.json"
port_arg = args['port'] or "8080"

port = 8080 if port_arg is None else int(port_arg)


class InstantAPIServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        path = self.path[1:]
        components = string.split(path, '/')

        try:
            node = json.loads(open(file_arg).read())
        except IOError:
            print "Couldn't find file '%s'" % file_arg
            sys.exit()

        for component in components:
            if len(component) == 0 or component == "favicon.ico":
                continue

            if type(node) == dict:
                node = node[component]

            elif type(node) == list:
                node = node[int(component)]

        self.wfile.write(json.dumps(node))

        return


try:
    server = HTTPServer(('', port), InstantAPIServer)
    print 'Starting instant API server on port %s...' % (port)
    server.serve_forever()

except KeyboardInterrupt:
    print 'Stopping instant API server...'
    server.socket.close()
