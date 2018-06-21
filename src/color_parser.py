
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

