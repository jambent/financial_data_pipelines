# make help
#
# The following commands can be used:
#
# init:		Installs required packages
# test:		Runs pytest on files in test folder
# coverage: Runs test coverage check against minimum level of 90%
# format:	Formats with autopep8 before checking results with flake8
# safety:	Runs safety
# bandit:	Runs bandit
# clean:	Removes __pycache__ and venv folders/files

define find.functions
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
endef

help:
	@echo 'The following commands can be used:'
	@echo ''
	$(call find.functions)


VENV = venv
PIP = $(VENV)/bin/pip
MINUMUM_COVERAGE = 90

.PHONY: init
init: ##	Installs required packages
init: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	python -m venv $(VENV)
	$(PIP) install -r requirements.txt


.PHONY: test
test: ##	Runs pytest on files in test folder
test:
	python -m pytest ./test

.PHONY: coverage
coverage: ##Runs test coverage check against minimum level of 90%
coverage:
	coverage run --omit 'venv/*' -m pytest && coverage report -m --fail-under=${MINUMUM_COVERAGE}

.PHONY: format
format: ##Formats with autopep8 before checking results with flake8
format:
	autopep8 --in-place --aggressive --aggressive --recursive ./src ./test --max-line-length 79
	flake8 ./src ./test

.PHONY: safety
safety: ##Runs safety
safety:
	safety check

.PHONY: bandit
bandit: ##Runs bandit
bandit:
	bandit ./src ./test

.PHONY: clean
clean: ##	Removes __pycache__ and venv folders/files
clean:
	rm -rf __pycache__
	rm -rf $(VENV)