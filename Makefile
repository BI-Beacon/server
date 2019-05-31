.PHONY: env

env/bin/activate: 
	python3 -m venv env
	( . env/bin/activate && pip install -r requirements.txt )

env: env/bin/activate

clean:
	rm -rf env

run: env
	( . env/bin/activate && python src/server.py 80 )

test: env
	( . env/bin/activate && python tst/test_server.py )
