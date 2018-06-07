all:	tests

tests:
	pylint3 *.py -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > pylint-report.txt || true
	pytest-3 --junitxml nosetests.xml .
	coverage run test_*.py
