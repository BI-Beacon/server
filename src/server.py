import sys

from flask import Flask, request
from flask_cors import CORS


flask_app = Flask(__name__)
CORS(flask_app)


@flask_app.route('/v1/<lampid>',
                 methods=["POST", "GET"],
                 strict_slashes=False)
def v1api(lampid):
	# TODO: GET
    v1api = V1API(post_packet)
    (json_obj, status) = v1api.handle(id=lampid, formdata=request.form)
    return json.dumps(json_obj), status


def run():
    if len(sys.argv) != 2:
        print("Usage: server.py <apiport>")
        return
    apiport = int(sys.argv[1])
    DEBUG = True
    flask_app.run(host='0.0.0.0',
                  port=apiport,
                  debug=DEBUG,
                  threaded=True)


if __name__ == '__main__':
    run()