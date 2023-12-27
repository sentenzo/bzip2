CODE_DIRS = app

lint:
	isort ${CODE_DIRS}
	black ${CODE_DIRS}
	flake8 ${CODE_DIRS} --count --select=E9,F63,F7,F82 --show-source --statistics

test:
	pytest -vsx -m "not slow"

test-all:
	pytest -vsx
