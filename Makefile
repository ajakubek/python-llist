.PHONY: clean test

all: clean build install test

build:
	python setup.py build

install:
	python setup.py install --install-lib ./tests

clean:
	python setup.py clean --all

test:
	python tests/llist_test.py

