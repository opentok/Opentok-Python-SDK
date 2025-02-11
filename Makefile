.PHONY: clean test dist coverage install requirements release release-test

clean:
	rm -rf dist build

coverage:
	pytest -v --cov=opentok
	coverage html

test:
	pytest -v

dist:
	python setup.py sdist --formats gztar bdist_wheel

check:
	twine check dist/*.whl

release:
	twine upload dist/*

install: requirements

requirements: .requirements.txt

.requirements.txt: requirements.txt
	python -m pip install --upgrade pip setuptools
	python -m pip install -r requirements.txt
	python -m pip freeze > .requirements.txt
