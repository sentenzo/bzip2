
APP_DIR = app
CODE_DIRS = ${APP_DIR} tests

run:
	python ${APP_DIR}/main.py

lint:
	isort ${CODE_DIRS}
	black ${CODE_DIRS}
	ruff check ${CODE_DIRS}
	poetry check

test:
	pytest -vsx -m "not slow"

test-all:
	pytest -vsx
