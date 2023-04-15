#
#  Author: Hari Sekhon
#  Date: 2016-01-17 12:56:53 +0000 (Sun, 17 Jan 2016)
#
#  vim:ts=4:sts=4:sw=4:noet
#
#  https://github.com/HariSekhon/Diagrams-as-Code
#
#  If you're using my code you're welcome to connect with me on LinkedIn and optionally send me feedback
#
#  https://www.linkedin.com/in/HariSekhon
#

# ===================
# bootstrap commands:

# setup/bootstrap.sh
#
# OR
#
# Alpine:
#
#   apk add --no-cache git make && git clone https://github.com/HariSekhon/DevOps-Python-tools pytools && cd pytools && make
#
# Debian / Ubuntu:
#
#   apt-get update && apt-get install -y make git && git clone https://github.com/HariSekhon/DevOps-Python-tools pytools && cd pytools && make
#
# RHEL / CentOS:
#
#   yum install -y make git && git clone https://github.com/HariSekhon/DevOps-Python-tools pytools && cd pytools && make

# ===================

ifneq ("$(wildcard bash-tools/Makefile.in)", "")
	include bash-tools/Makefile.in
endif

REPO := HariSekhon/Diagrams-as-Code

CODE_FILES := $(shell git ls-files | grep -E -e '\.sh$$' -e '\.py$$' | sort)

main: graphs
	@:

.PHONY: graphs
graphs:
	@echo =================
	@echo Generating Graphs
	@echo =================
	for x in *.py; do python3 $$x; done

.PHONY: build
build: init
	@echo ================
	@echo Diagrams Build
	@echo ================
	@$(MAKE) git-summary
	@echo
	# defer via external sub-call, otherwise will result in error like
	# make: *** No rule to make target 'python-version', needed by 'build'.  Stop.
	@$(MAKE) python-version

	if [ -z "$(CPANM)" ]; then make; exit $$?; fi
	$(MAKE) system-packages-python

	$(MAKE) python

.PHONY: init
init:
	@echo "running init:"
	git submodule update --init --recursive
	@echo

.PHONY: install
install: build
	@:

.PHONY: python
python:
	@PIP=$(PIP) PIP_OPTS="--ignore-installed" bash-tools/python_pip_install_if_absent.sh requirements.txt
	@echo
	$(MAKE) pycompile
	@echo
	@echo 'BUILD SUCCESSFUL (Diagrams)'

.PHONY: test
test:
	bash-tools/check_all.sh

.PHONY: clean
clean:
	@rm -fv -- *.pyc *.pyo
