PKGNAME := code-empire-forum
PREFIX := $(CURDIR)/debian/$(PKGNAME)
BINPATH := $(PREFIX)/opt/checkio/forum
EXCLUDES := excludes.txt
RSYNC := rsync --exclude-from $(EXCLUDES) -va
REQUIREMENTS := requirements.txt
PYTHON := /opt/python/bin/python2.7

.PHONY : install clean

clean:
	MD5OK=`eval md5sum -c requirements.md5 >/dev/null; echo $$?` ;\
	if [ "x$$MD5OK" != "x0" ] ; then rm -f requirements.md5 ; fi

requirements.md5:
	virtualenv --python=$(PYTHON) --no-site-packages $(BINPATH)
	$(BINPATH)/bin/pip install -r $(CURDIR)/$(REQUIREMENTS)
	md5sum $(CURDIR)/$(REQUIREMENTS) > requirements.md5

install: requirements.md5
	mkdir -p $(BINPATH)
	mkdir -p $(BINPATH)/logs
	$(RSYNC) $(CURDIR)/* $(BINPATH)
	echo $(GIT_COMMIT) > $(BINPATH)/$(PKGNAME)_version.txt

