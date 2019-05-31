import unittest
from pprint import pformat
import time
import subprocess

import approvaltests
from approvaltests.combination_approvals import verify_all_combinations
from approvaltests.reporters.generic_diff_reporter_factory import GenericDiffReporterFactory

from context import server
import reuseaddr_hack
from io import StringIO


def get_process_output_for_inputs(port, request_list):
    cmdline = [
        'python', 'src/server.py'
    ]
    if port:
        cmdline.append(str(port))

    stdout = open('/tmp/output.txt', 'w')
    stderr = open('/tmp/error.txt', 'w')
    process = subprocess.Popen(
        cmdline,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(0.4)
    process.terminate()
    sout, serr = process.communicate(timeout=2)

    # process.wait(timeout=2)

    # stdout.close()
    # stderr.close()

    # with open('/tmp/output.txt') as f:
    #     sout = f.read()
    # with open('/tmp/error.txt') as f:
    #     serr = f.read()
import unittest
from pprint import pformat
import time
import subprocess

import approvaltests
from approvaltests.combination_approvals import verify_all_combinations
from approvaltests.reporters.generic_diff_reporter_factory import GenericDiffReporterFactory

from context import server
import reuseaddr_hack
from io import StringIO


def get_process_output_for_inputs(port, request_list):
    cmdline = [
        'python', 'src/server.py'
    ]
    if port:
        cmdline.append(str(port))

    process = subprocess.Popen(
        cmdline,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(0.4)
    process.terminate()
    sout, serr = process.communicate(timeout=2)

    return {
        'stdout': sout.decode('ascii'),
        'stderr': serr.decode('ascii'),
        'returncode': process.returncode
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
            [None, 8890],
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


# if __name__ == '__main__':
#     unittest.main()

    return {
        'stdout': sout,
        'stderr': serr,
        'returncode': process.returncode
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
            [None, 9999],
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
        result=pformat(result, width=6000, indent=2)
    )


# if __name__ == '__main__':
#     unittest.main()
