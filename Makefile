TOPTARGETS := all clean setup tests
SUBDIRS := src

$(TOPTARGETS): $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@ $(MAKECMDGOALS)

clean:
	rm -f *~

.PHONY: $(TOPTARGETS) $(SUBDIRS)
