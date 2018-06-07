TOPTARGETS := all clean setup
SUBDIRS := 

$(TOPTARGETS): $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@ $(MAKECMDGOALS)

clean:
	rm -f *~

.PHONY: $(TOPTARGETS) $(SUBDIRS)
