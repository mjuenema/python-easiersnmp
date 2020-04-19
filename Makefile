

NOSE := nosetests --failed --verbose --no-byte-compile --logging-level=DEBUG --detailed-errors
#COVERAGE := $(NOSE) --with-coverage --cover-package=terrascript --cover-erase --cover-branches --cover-html
#FLAKE8 := python3 -m flake8

all:
	@echo "make test"
	@echo "make debug"

test: clean
	$(NOSE) tests/*.py


debug: clean
	$(NOSE) --pdb tests/*.py

clean:
	@[ -f .noseids ] && rm -f .noseids
    
