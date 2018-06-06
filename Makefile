TOPTARGETS := all clean setup
SUBDIRS := docs

$(TOPTARGETS): $(SUBDIRS)
$(SUBDIRS):
	pipenv run $(MAKE) -C $@ $(MAKECMDGOALS)

clean:
	rm -f *~

.PHONY: $(TOPTARGETS) $(SUBDIRS)
