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

#include Makefile.in

REPO := HariSekhon/Diagrams-as-Code

CODE_FILES := $(shell git ls-files | grep -E -e '\.sh$$' -e '\.py$$' | sort)

.PHONY: build
build:
	@echo ================
	@echo Bash Tools Build
	@echo ================
	@$(MAKE) git-summary
	@$(MAKE) init

.PHONY: init
init: git
	@echo "running init:"
	git submodule update --init --recursive
	@echo

.PHONY: install
install: build
	@:

.PHONY: test
test:
	./check_all.sh

.PHONY: clean
clean:
	@rm -fv -- *.pyc *.pyo
