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
	poetry run python setup.py bdist_wheel

clean: clean-build clean-pyc

clean-build:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf .tox
	rm -rf .coverage*

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '.pytest_cache' -exec rm -rf {} +
tox:
	@tox

flake:
	@poetry run flake8

test:
	@poetry run pytest $(add)

install:
	@poetry run pip install -e .

uninstall:
	@poetry run pip uninstall horn-py

upload:
	@poetry run twine upload dist/*

pypi: clean pkg upload
