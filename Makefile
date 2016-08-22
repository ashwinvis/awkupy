
help:
	@echo "targets: develop, and tests"

develop:
	python setup.py develop

tests:
	python -m unittest discover


