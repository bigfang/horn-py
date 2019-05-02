help:
	@echo "pkg - package python wheel"
	@echo "clean - remove build/python artifacts"
	@echo "flake - check style with flake8"
	@echo "install - install for development"
	@echo "uninstall - uninstall for development"

pkg:
	pipenv run python setup.py sdist bdist_wheel

clean: clean-build clean-pyc

clean-build:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '.pytest_cache' -exec rm -rf {} +

flake:
	pipenv run flake8 --config=setup.cfg horn

install:
	pip install -e .

uninstall:
	pip uninstall horn-py
