
help:
	@echo "targets: install, develop, and tests"

install:
	pip install .

develop:
	pip install -e .[dev]

tests:
	python -m unittest discover

dist:
	python setup.py bdist_wheel
	python setup.py sdist

release: dist ## package and upload a release
	twine upload dist/*

dist-check: dist ## package and verify it
	twine check dist/*

dist-clean:
	rm -rf build/ dist/
