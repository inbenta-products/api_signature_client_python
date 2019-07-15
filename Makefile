# Minimal makefile 
#
install:
	python -m pip install .

tests:
	python setup.py test

coverage:
	python -m coverage run -m pytest tests
	python -m coverage report -m
