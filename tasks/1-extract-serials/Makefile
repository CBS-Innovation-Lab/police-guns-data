SUBDIRS := $(wildcard */.)

.PHONY: all $(SUBDIRS)

all: $(SUBDIRS)

$(SUBDIRS):
	$(MAKE) -C $@

cleanup:
	find . -type f -path "*/output/*" -delete