all:	setup tests

setup:
	pipenv install --dev

tests:
	pipenv run pylint *.py -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > pylint-report.txt || true
	pipenv run pytest --junitxml nosetests.xml .
	pipenv run coverage run test_*.py
