.PHONY: clean run test

env/bin/activate:
	python3 -m venv env
	( . env/bin/activate && pip install -r requirements.txt )

env: env/bin/activate

.devenv: env
	( . env/bin/activate && pip install -r requirements-dev.txt )
	sudo apt-get install meld
	touch .devenv

clean:
	rm -rf env
	rm -rf src/__pycache__
	rm -rf tst/__pycache__
	rm -rf .pytest_cache
	rm .devenv

run: env
	( . env/bin/activate && python src/server.py 80 )

test: .devenv
	( . env/bin/activate && pytest tst )
