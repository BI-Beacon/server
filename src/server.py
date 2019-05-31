import sys

from flask import Flask


VERSION = 0.1


def run():

    if len(sys.argv) != 2:
        print("Usage: server.py <port>")
        print(" port: REST API requests will be available at this port.")
        return

    port = int(sys.argv[1])

    print("BI-Beacon version {version} starting.".format(version=VERSION))
    print("Using port: {port}".format(port=port))

    flask_app = Flask(__name__)
    flask_app.run(host='0.0.0.0',
                  port=port,
                  debug=False,
                  threaded=True)
    print("Server stopped.")


if __name__ == '__main__':
    run()
