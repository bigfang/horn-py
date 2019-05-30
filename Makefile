help:
	@echo "pkg - package python wheel"
	@echo "clean - remove built python artifacts"
	@echo "flake - check style with flake8"
	@echo "test - run unit tests"
	@echo "tox - run tox"
	@echo "install - install for development"
	@echo "uninstall - uninstall for development"
	@echo "upload - upload to pypi"
	@echo "pypi - clean package and upload"

pkg:
	pipenv run python setup.py bdist_wheel

clean: clean-build clean-pyc

clean-build:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf .tox

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '.pytest_cache' -exec rm -rf {} +
tox:
	@tox

flake:
	@pipenv run flake8

test:
	@pipenv run py.test $(add)

install:
	@pip install -e .

uninstall:
	@pip uninstall horn-py

upload:
	@pipenv run twine upload dist/*

pypi: clean pkg upload
