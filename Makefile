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
#   apk add --no-cache git make && git clone https://github.com/HariSekhon/Diagrams-as-Code diagrams && cd diagrams && make
#
# Debian / Ubuntu:
#
#   apt-get update && apt-get install -y make git && git clone https://github.com/HariSekhon/Diagrams-as-Code diagrams && cd diagrams && make
#
# RHEL / CentOS:
#
#   yum install -y make git && git clone https://github.com/HariSekhon/Diagrams-as-Code diagrams && cd diagrams && make

# ===================

ifneq ("$(wildcard bash-tools/Makefile.in)", "")
	include bash-tools/Makefile.in
endif

REPO := HariSekhon/Diagrams-as-Code

CODE_FILES := $(shell git ls-files | grep -E -e '\.d2$$' -e '\.sh$$' -e '\.py$$' | sort)

SHELL := /usr/bin/env bash

main:
	@$(MAKE) diag

.PHONY: diag
diag: diagrams
	@:

.PHONY: graphs
graphs: diag
	@:

.PHONY: diagrams
diagrams: diagrams-python diagrams-d2
	@:

.PHONY: diagrams-python
diagrams-python:
	@if ! type -P dot >/dev/null 2>&1 || \
		! python3 -c 'import diagrams' 2>&1; then \
		$(MAKE) install-python; \
	fi
	@echo ==========================
	@echo Generating Python Diagrams
	@echo ==========================
	mkdir -p -v images
	$(MAKE) clean
	@set -o pipefail; \
	set -eu; \
	export CI=1; \
	exitcode=0; \
	for x in *.py; do \
		if [ "$$x" = template.py ]; then \
			continue; \
		fi; \
		img="images/$${x%.py}.svg"; \
		echo "Generating $$x -> $$img"; \
		if ! python3 $$x; then \
			git checkout "$$img" || rm -fv "$$img"; \
			exitcode=1 ;\
		fi; \
	done; \
	exit "$$exitcode"
	@# generating images straight into images/ dir now to skip one step and avoid local run tidying being required
	@#sleep 1  # give the last png a second to be opened before moving it to avoid an error
	@#mv -fv *.png images/

.PHONY: diagrams-d2
diagrams-d2: clean
	@if ! type -P d2 >/dev/null 2>&1; then \
		echo; \
		$(MAKE) install-d2; \
	fi
	@echo
	bash-tools/diagrams/d2_generate_diagrams.sh

.PHONY: diagrams-mermaidjs
diagrams-mermaidjs:
	@if ! type -P mmdc >/dev/null 2>&1; then \
		$(MAKE) install-mermaidjs; \
	fi;
	@echo =============================
	@echo Generating MermaidJS Diagrams
	@echo =============================
	mkdir -p -v images
	$(MAKE) clean
	@set -o pipefail; \
	set -eu; \
	for x in *.mmd; do \
		if [ "$$x" = template.mmd ]; then \
			continue; \
		fi; \
		img="images/$${x%.mmd}.svg"; \
		echo "Generating $$x -> $$img"; \
		if ! mmdc -i "$$x" -o "$$img" ; then \
			git checkout "$$img" || rm -fv "$$img"; \
			exitcode=1; \
		fi; \
	done; \
	exit "$$exitcode"

.PHONY: mmdc
mmdc: diagrams-mermaidjs
	@:

.PHONY: d2
d2: diagrams-d2
	@:

.PHONY: py
py: diagrams-python
	@:

.PHONY: install
install: build
	@:

.PHONY: build
build: init
	@echo ==============
	@echo Diagrams Build
	@echo ==============
	@$(MAKE) git-summary
	@echo
	@$(MAKE) d2
	@echo
	@$(MAKE) py

.PHONY: init
init:
	@echo "running init:"
	git submodule update --init --recursive
	@echo

.PHONY: install-d2
install-d2:
	@echo ==============
	@echo Install D2
	@echo ==============
	bash-tools/install/install_d2.sh
	@# don't install this, see DevOps-Bash-tools install/install_d2.sh for details why
	@#curl -fsSL https://d2lang.com/install.sh | sh -s -- --tala

.PHONY: install-mermaidjs
install-mermaidjs:
	@echo =================
	@echo Install MermaidJS
	@echo =================
	@if ! type -P mmdc >/dev/null 2>&2; then \
		bash-tools/packages/install_packages_if_not_installed.sh nodejs; \
		bash-tools/packages/nodejs_npm_install_if_absent.sh @mermaid-js/mermaid-cli; \
	fi

.PHONY: install-python
install-python:
	@echo ==============
	@echo Install Python
	@echo ==============
	# defer via external sub-call, otherwise will result in error like
	# make: *** No rule to make target 'python-version', needed by 'build'.  Stop.
	@$(MAKE) python-version

	if [ -z "$(CPANM)" ]; then make; exit $$?; fi
	$(MAKE) system-packages-python

	$(MAKE) python

.PHONY: python
python:
	@PYTHON=python3 PIP=pip3 PIP_OPTS="--ignore-installed" bash-tools/python/python_pip_install_if_absent.sh requirements.txt
	@echo
	@#$(MAKE) pycompile
	@echo
	@echo 'BUILD SUCCESSFUL (Diagrams)'

.PHONY: test
test: diagrams
	PYTHON=python3 bash-tools/checks/check_all.sh

.PHONY: clean
clean:
	@echo
	@echo "Git resetting images/ dir:"
	@echo
	git checkout images
	@echo
	@echo
	@echo "Removing *.pyc / *.pyo files:"
	@echo
	@rm -fv -- *.pyc *.pyo
	@echo
	@echo "Removing PNG / SVG files:"
	@echo
	@rm -fv -- *.png *.svg custom/*.png custom/*.svg
	@echo
	@echo "Removing intermediate dot files of the same name as Python files but without the prefix:"
	@for x in *.py; do rm -fv -- "$${x%.py}"; done
	@echo
	@#git status --porcelain --ignored | awk '/^!!/{print $2}' | xargs rm -fv --

.PHONY: fmt
fmt: init
	d2 fmt *.d2 custom/*.d2

	# put shebang header back to normal to work around this bug:
	#
	#   https://github.com/terrastruct/d2/issues/1319
	#
	sleep 1
	if uname -s | grep Darwin; then \
		sed(){ gsed "$$@"; }; \
	fi; \
	sed -i 's|# !/|#!/|' *.d2 custom/*.d2 templates/*.d2

	# revert typechange of template.d2 symlink
	for directory in . templates; do \
		pushd "$$directory" && \
		git checkout $$(git status --porcelain | awk '/^.T/{print $$2}') && \
		popd || \
		exit 1; \
	done

# set CODE_FILES extensions at the top instead to reuse the better wc in bash-tools/Makefile.in
#.PHONY: wc
#wc:
#    wc -l *.d2 *.py
