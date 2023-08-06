.PHONY: clean clean-test clean-pyc clean-build  dist install doc-deps doc-api doc-build public release help
.DEFAULT_GOAL := help

DOCDIR                  ?= doc
APIDOC                   = rxdata rxdata.typeguard

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
    match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
    if match:
       target, help = match.groups()
       print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr report/

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +


clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr .tox/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

dist: clean ## builds source and wheel package
	@python setup.py sdist
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	@python setup.py install

doc-deps: ## build doc deps
	pip3 install -r requirements-doc.txt
	pip3 install -r requirements.txt

doc-api: doc-deps ## build doc api
	rm -fr ${DOCDIR}/rxdata
	pdoc --force -o ${DOCDIR} $(APIDOC)

doc-build: doc-deps doc-api ## make doc build
	python ${DOCDIR}/script/toc/mkdocs.py ${DOCDIR}/mkdocs_.yml ${DOCDIR}/mkdocs.yml ${APIDOC} > ${DOCDIR}/mkdocs.yml
	python ${DOCDIR}/script/toc/markdown.py README.md ${APIDOC} > ${DOCDIR}/index.md
	cd ${DOCDIR} && mkdocs build -c -f mkdocs.yml

public: doc-build ## publish docs

release: dist ## package and upload a release
	pip install --upgrade-strategy only-if-needed twine
	twine upload dist/*
