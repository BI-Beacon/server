TOPTARGETS := all clean setup
SUBDIRS := docs

$(TOPTARGETS): $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@ $(MAKECMDGOALS)

clean:
	rm -f *~

.PHONY: $(TOPTARGETS) $(SUBDIRS)
