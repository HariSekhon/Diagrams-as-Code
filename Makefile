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

CODE_FILES := $(shell git ls-files | grep -E -e '\.sh$$' -e '\.py$$' | sort)

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
	export CI=1; \
	for x in *.py; do \
		if [ "$$x" = template.py ]; then \
			continue; \
		fi; \
		echo "Generating $$x"; \
		python3 $$x; \
	done
	@# generating images straight into images/ dir now to skip one step and avoid local run tidying being required
	@#sleep 1  # give the last png a second to be opened before moving it to avoid an error
	@#mv -fv *.png images/

.PHONY: diagrams-d2
diagrams-d2:
	@if ! type -P d2 >/dev/null 2>&1; then \
		$(MAKE) install-d2; \
	fi;
	@echo ======================
	@echo Generating D2 Diagrams
	@echo ======================
	mkdir -p -v images
	$(MAKE) clean
		# can't use shebang in d2 yet to automate differently themed diagrams because d2 doesn't currently support defining
		# the theme in the .d2 file and also doesn't support having a separate images/ directory, see:
		#
		#	https://github.com/terrastruct/d2/issues/1286
		#
		#	https://github.com/terrastruct/d2/issues/1287
		#
		#	https://github.com/terrastruct/d2/issues/1288
		#
		#if [ -x "$$x" ]; then
		#    ./"$$x"
		#fi
	for x in *.d2; do \
		if [ "$$x" = template.d2 ]; then \
			continue; \
		fi; \
		img="images/$${x%.d2}.svg"; \
		echo "Generating $$x -> $$img"; \
		d2 --theme 200 "$$x" "$$img"; \
	done

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
	curl -fsSL https://d2lang.com/install.sh | sh -s --

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
	@PYTHON=python3 PIP=pip3 PIP_OPTS="--ignore-installed" bash-tools/python_pip_install_if_absent.sh requirements.txt
	@echo
	@#$(MAKE) pycompile
	@echo
	@echo 'BUILD SUCCESSFUL (Diagrams)'

.PHONY: test
test:
	PYTHON=python3 bash-tools/check_all.sh

.PHONY: clean
clean:
	@echo "Removing any stray PNGs or *.pyc *.pyo files:"
	@rm -fv -- *.pyc *.pyo *.png *.svg
	@echo "Removing any leftover dot files:"
	@for x in *.py; do rm -fv "$${x%.py}"; done
