TOPTARGETS := all clean setup tests
SUBDIRS := src

$(TOPTARGETS): $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@ $(MAKECMDGOALS)

clean:
	rm -f *~ golint-report.out

.PHONY: $(TOPTARGETS) $(SUBDIRS)
