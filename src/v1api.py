# coding: utf-8
import re
import struct

from color_parser import parse_color

COLOR = 'color'
PERIOD = 'period'
INT_RE = re.compile('^[0-9]{0,10}$')
ID_RE = re.compile('^[-_0-9a-zA-Z]{1,80}$')
assert ID_RE.match('a')
assert ID_RE.match('123')
assert ID_RE.match('1292-ABCdbf')
assert ID_RE.match('__')
assert not ID_RE.match('##')



def valid_id(id):
    return ID_RE.match(id)


def error(msg):
    json = {'message': msg}
    return (json, 400)


def success(msg):
    json = {'message': msg}
    return (json, 200)


class V1API(object):

    def __init__(self, post_packet):
        self.post_packet = post_packet

    def handle(self, id, formdata):

        if not valid_id(id):
            return error("Invalid id")

        if COLOR not in formdata:
            return error("Expected color data")

        known_parameters = [COLOR, PERIOD]
        for p in formdata:
            if p not in known_parameters:
                return error("Unknown parameter '%s'" % p)

        try:
            color = parse_color(formdata[COLOR])
        except ValueError:
            return error("Invalid color")

        hz = None
        if PERIOD in formdata:
            period = formdata[PERIOD]
            if not INT_RE.match(period):
                return error("Invalid period")
            period = int(period) if period else 0
            hz = 1000.0 / int(period) if period else None

        packet = tuple(list(color) + [hz]) if hz else color

        self.post_packet(id, tuple(packet))

        return success("'%s' updated" % id)
