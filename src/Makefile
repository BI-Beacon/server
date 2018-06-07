all:	setup tests

setup:
	pipenv install

tests:
	pipenv run pylint3 *.py -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > pylint-report.txt || true
	pipenv run pytest-3 --junitxml nosetests.xml .
	pipenv run coverage run test_*.py
