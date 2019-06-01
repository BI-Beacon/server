# Standard
import sys
import json

# Third-party
from flask import Flask, request

# Local
from v1api import V1API


VERSION = 0.1
APPNAME = 'BI-Beacon Open Source Server'

state = {}

flask_app = Flask(APPNAME)


def tuple2command(tup):
    if len(tup) == 3:
        return 'color %d %d %d\n' % tup
    else:
        return 'pulse_1 %d %d %d %1.2f\n' % tup

assert tuple2command((0, 100, 0)) == 'color 0 100 0\n'
assert tuple2command((1, 2, 3, 1.5)) == 'pulse_1 1 2 3 1.50\n'


@flask_app.route(
'/<channelkey>',
    methods=["POST", "GET"]
)
def beacon_api(channelkey):
    if request.method == 'GET':
        tuple = state[channelkey] if channelkey in state else (0, 255, 0)
        resp = tuple2command(tuple)
        print("Responding with {resp}".format(resp=resp))
        return resp
    if request.method == 'POST':
        def update_state(channelkey, tuple):
            state[channelkey] = tuple
        v1api_handler = V1API(update_state)
        (json_obj, status) = v1api_handler.handle(id=channelkey, formdata=request.form)
        return json.dumps(json_obj), status


def run():

    if len(sys.argv) != 2:
        print("Usage: server.py <port>")
        print(" port: REST API requests will be available at this port.")
        return

    port = int(sys.argv[1])

    print("BI-Beacon version {version} starting.".format(version=VERSION))
    print("Using port: {port}".format(port=port))

    flask_app.run(host='0.0.0.0',
                  port=port,
                  debug=False,
                  threaded=True)
    print("Server stopped.")


if __name__ == '__main__':
    run()
