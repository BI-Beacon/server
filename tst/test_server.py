from pprint import pformat
import random
import subprocess
import time
import unittest

import approvaltests
from approvaltests.combination_approvals import verify_all_combinations
from approvaltests.reporters.generic_diff_reporter_factory import GenericDiffReporterFactory
import requests

import reuseaddr_hack
from io import StringIO


def get_process_output_for_inputs(port, request_list):
    cmdline = [
        'python', 'src/server.py'
    ]
    if port is not None:
        cmdline.append(str(port))

    process = subprocess.Popen(
        cmdline,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    time.sleep(0.33)  # @refactor look for magic string instead of hard coded wait

    # run requests
    responses = []
    if port is not None:
        for req in request_list:
            method, url = req[:2]
            url = "http://localhost:{port}/{url}".format(url=url, port=port)
            if method == 'GET':
                responses.append(requests.get(url))
            if method == 'POST':
                responses.append(requests.post(url, req[2]))

    process.terminate()
    sout, _ = process.communicate(timeout=0.1)  # @refactor more robust method than timeout?

    def clean_line(line):
        if '[' and ']' in line:
            begin = line.partition('[')[0] + '['
            end = ']' + line.partition(']')[2]
            return begin + end
        else:
            return line

    assert (
        clean_line('127.0.0.1 - - [31/May/2019 19:48:12] "GET /test HTTP/1.1" 404 -')
             ==
                   '127.0.0.1 - - [] "GET /test HTTP/1.1" 404 -'
    )

    sout = sout.decode('ascii')
    stdout = [clean_line(line) for line in sout.splitlines()]
    responses = [r.content.decode('ascii') for r in responses]

    return {
        'stdout': stdout,
        'returncode': process.returncode,
        'responses': responses
    }


class TestServer(unittest.TestCase):

    def setUp(self):
        factory = GenericDiffReporterFactory()
        import os
        print(os.getcwd())
        factory.load('tst/reporters.json')
        self.reporter = factory.get('meld')

    def test_server_process(self):
        inputs = [
            [None, 8989],
            [
                [
                    ('GET', 'test'),
                    ('POST', 'test', {'color': '#ff00ff'}),
                    ('GET', 'test')
                ]
            ]
        ]
        verify_all_combinations(
            get_process_output_for_inputs,
            inputs,
            reporter=self.reporter,
            formatter=result_formatter)


def result_formatter(args, result):
    return '\nGiven: {args}\nGot:\n{result}\n'.format(
        args=pformat(args),
        result=pformat(result, width=60, indent=2)
    )

