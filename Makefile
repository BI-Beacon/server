.PHONY: clean run test

env/bin/activate:
	python3 -m venv env
	( . env/bin/activate && pip install -r requirements.txt )

env: env/bin/activate

.devenv: env
	( . env/bin/activate && pip install -r requirements-dev.txt )
	touch .devenv

clean:
	$(RM) -rf env
	$(RM) -rf src/__pycache__
	$(RM) -rf tst/__pycache__
	$(RM) -rf .pytest_cache
	$(RM) .devenv

test: .devenv
	( . env/bin/activate && pytest tst )
