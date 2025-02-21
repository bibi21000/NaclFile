#!/usr/bin/make -f
-include makefile.local

ifndef PYTHON
PYTHON:=python3
endif

.PHONY: venv tests

venv:
	${PYTHON} -m venv venv
	./venv/bin/pip install .
	./venv/bin/pip install .[test]
	./venv/bin/pip install .[zstd]
	./venv/bin/pip install .[build]
	./venv/bin/pip install .[doc]

build:
	rm -rf dist
	./venv/bin/python3 -m build

testpypi:
	./venv/bin/python3 -m twine upload --repository testpypi --verbose dist/*

doc:
	./venv/bin/pdoc --output-directory docs naclfile/zstd.py naclfile/tar.py naclfile/__init__.py

pypi:
	./venv/bin/python3 -m twine upload --repository pypi --verbose dist/*

ruff:
	./venv/bin/ruff check naclfile/

bandit:
	./venv/bin/bandit -r naclfile

tests:
	./venv/bin/pytest  --random-order -n auto tests/
