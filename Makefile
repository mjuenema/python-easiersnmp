

NOSE := nosetests --failed --verbose --no-byte-compile --logging-level=DEBUG --detailed-errors
#COVERAGE := $(NOSE) --with-coverage --cover-package=terrascript --cover-erase --cover-branches --cover-html
#FLAKE8 := python3 -m flake8

all:
	@echo "make build        "
	@echo "make testpublish  - Publish to TesPyPi"
	@echo "make publish      - Publish to PyPi"

build:
	poetry build

testpublish: build
	 poetry publish -r test-pypi

publish: build
	 poetry publish

#test: clean
#	$(NOSE) tests/*.py
#
#
#debug: clean
#	$(NOSE) --pdb tests/*.py
#
#clean:
#	@[ -f .noseids ] && rm -f .noseids
    
