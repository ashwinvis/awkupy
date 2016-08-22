
help:
	@echo "targets: install, develop, and tests"

install:
	python setup.py install

develop:
	python setup.py develop

tests:
	python -m unittest discover


