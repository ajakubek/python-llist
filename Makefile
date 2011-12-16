.PHONY: clean test 

all: clean build install test

build:
	python setup.py build

install:
	sudo python setup.py install

clean:
	rm -rf build

test:
	python tests/llist_test.py

