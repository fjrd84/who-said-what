run:
	python3 main.py

init:
	pip3 install -r requirements.txt; python3 -m spacy.en.download all

test:
	export PYTHONPATH=.;pytest tests -v

watchtest:
	export PYTHONPATH=.;pytest-watch . --ignore venv

coverage:
	nosetests --with-coverage --cover-erase --cover-html --cover-package=engines

clean:
	find . -name "*.pyc" -exec rm -f {} \;


.PHONY: init test coverage run clean watchtest
