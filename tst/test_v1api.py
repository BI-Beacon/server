# coding: utf-8

import unittest
from src.v1api import V1API, parse_color


class TestColorParse(unittest.TestCase):

    def test_black_is_correct(self):
        self.assertEqual((0, 0, 0), parse_color('#000000'))

    def test_white_is_correct(self):
        self.assertEqual((255, 255, 255), parse_color('#FFFFFF'))

    def test_green_is_correct(self):
        self.assertEqual((0, 255, 0), parse_color('#00ff00'))

    def test_initial_hash_is_optional(self):
        self.assertEqual((0, 255, 0), parse_color('00ff00'))

    def test_invalid_throws(self):
        self.assertRaises(ValueError, parse_color, '#000')
        self.assertRaises(ValueError, parse_color, '#0ff00o')


class TestV1API(unittest.TestCase):

    def test_bad_formdata(self):
        def post_packet(lampid, packet):
            pass
        (json, errcode) = V1API(post_packet).handle(id='lamp', formdata={})
        self.assertEqual(400, errcode)
        self.assertEqual("Expected color data", json['message'])

    def test_bad_id(self):
        def post_packet(lampid, packet):
            pass
        api = V1API(post_packet)
        (json, errcode) = api.handle(id='%%%', formdata={'color': '#ff00ff'})
        self.assertEqual(400, errcode)
        self.assertEqual("Invalid id", json['message'])

    def test_green_color(self):
        sent = []

        def post_packet(lampid, packet):
            sent.append(lampid)
            sent.append(packet)

        api = V1API(post_packet)
        (json, errcode) = api.handle(id='lamp', formdata={'color': "#00ff00"})
        self.assertEqual(200, errcode)
        self.assertEqual("'lamp' updated", json['message'])
        self.assertEqual('lamp', sent[0])
        self.assertEqual((0, 255, 0), sent[1])

    def test_red_color(self):
        sent = []

        def post_packet(lampid, packet):
            sent.append(lampid)
            sent.append(packet)

        api = V1API(post_packet)
        (json, errcode) = api.handle(id='lamp2', formdata={'color': "#ff0000"})
        self.assertEqual(200, errcode)
        self.assertEqual("'lamp2' updated", json['message'])
        self.assertEqual('lamp2', sent[0])
        self.assertEqual((255, 0, 0), sent[1])

    def test_yellow_pulse(self):
        sent = []

        def post_packet(lampid, packet):
            sent.append(lampid)
            sent.append(packet)

        api = V1API(post_packet)
        data = {'color': "#ffff00", 'period': '1000'}
        (json, errcode) = api.handle(id='lamp33', formdata=data)
        self.assertEqual(200, errcode)
        self.assertEqual("'lamp33' updated", json['message'])
        self.assertEqual('lamp33', sent[0])
        self.assertEqual((255, 255, 0, 1.0), sent[1])

    def test_invalid_color_spec(self):
        def post_packet(lampid, packet):
            pass
        (json, errcode) = V1API(post_packet).handle(id='lamp',
                                                    formdata={'color': "XYZ"})
        self.assertEqual(400, errcode)
        self.assertEqual("Invalid color", json['message'])

    def test_invalid_period(self):
        def post_packet(lampid, packet):
            pass
        data = {'color': "#00ff00", 'period': 'abc'}
        (json, errcode) = V1API(post_packet).handle(id='lamp',
                                                    formdata=data)
        self.assertEqual(400, errcode)
        self.assertEqual("Invalid period", json['message'])

    def test_unknown_form_parameter(self):
        def post_packet(lampid, packet):
            pass
        data = {'color': "#00ff00", 'huh': '123'}
        (json, errcode) = V1API(post_packet).handle(id='lamp',
                                                    formdata=data)
        self.assertEqual(400, errcode)
        self.assertEqual("Unknown parameter 'huh'", json['message'])

    def test_period_zero_means_no_period(self):
        sent = []

        def post_packet(lampid, packet):
            sent.append(lampid)
            sent.append(packet)

        data = {'color': "#ff00ff", 'period': '0'}
        (json, errcode) = V1API(post_packet).handle(id='lamp3',
                                                    formdata=data)
        self.assertEqual(200, errcode)
        self.assertEqual("'lamp3' updated", json['message'])
        self.assertEqual('lamp3', sent[0])
        self.assertEqual((255, 0, 255), sent[1])

    def test_period_empty_means_no_period(self):
        sent = []

        def post_packet(lampid, packet):
            sent.append(lampid)
            sent.append(packet)

        data = {'color': "#ff00ff", 'period': ''}
        (json, errcode) = V1API(post_packet).handle(id='lamp4',
                                                    formdata=data)
        self.assertEqual(200, errcode)
        self.assertEqual("'lamp4' updated", json['message'])
        self.assertEqual('lamp4', sent[0])
        self.assertEqual((255, 0, 255), sent[1])

if __name__ == '__main__':
    unittest.main()
