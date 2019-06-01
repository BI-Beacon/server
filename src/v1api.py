# coding: utf-8
import re
import logging

# Extension system
try:
    from customize import before_post_packet
except ImportError:
    def before_post_packet(*_):
        pass

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


ID_RE = re.compile('^[-_0-9a-zA-Z]{1,80}$')
assert ID_RE.match('a')
assert ID_RE.match('123')
assert ID_RE.match('1292-ABCdbf')
assert ID_RE.match('__')
assert not ID_RE.match('##')

INT_RE = re.compile('^[0-9]{0,10}$')

COLOR = 'color'
PERIOD = 'period'


def parse_color(s):

    if len(s) > 0 and s[0] != '#':
        s = '#' + s

    if len(s) != 7:
        raise ValueError()

    components = s[1:]

    def take2(s, ix):
        return s[ix:ix+2]

    def to256(s):
        return int(s, 16)

    result = []
    for i in range(0, 6, 2):
        result.append(take2(components, i))
    result = map(to256, result)

    return tuple(result)


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

        log.debug("Posting packet %s to %s", packet, id)
        before_post_packet(id, packet)
        self.post_packet(id, tuple(packet))

        return success("'%s' updated" % id)
