import unittest
from pprint import pformat
import subprocess

import approvaltests
from approvaltests.combination_approvals import verify_all_combinations
from approvaltests.reporters.generic_diff_reporter_factory import GenericDiffReporterFactory

from context import server


def get_server_stdout_for_inputs(port, request_list):
    cmdline = [
        # '/bin/ls', '/'
        'python', 'src/server.py', '80'
    ]
    print(cmdline)
    result = subprocess.run(cmdline, stdout=subprocess.PIPE)
    return result.stdout.decode('ascii').splitlines()


class TestServer(unittest.TestCase):

    def setUp(self):
        factory = GenericDiffReporterFactory()
        import os
        print(os.getcwd())
        factory.load('tst/reporters.json')
        self.reporter = factory.get('meld')

    def test_server_process(self):
        inputs = [
            [80, 8888],
            [
                [
                    ('GET', 'test'),
                    ('POST', 'test', {'color': '#ff00ff'}),
                    ('GET', 'test')
                ]
            ]
        ]
        verify_all_combinations(
            get_server_stdout_for_inputs,
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
