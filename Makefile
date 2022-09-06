# Minimal makefile 
#
install:
	python -m pipenv install .

enter:
	python -m pipenv shell

tests:
	python -m pytest -vv

coverage:
	python -m coverage run -m pytest tests
	python -m coverage report -m
