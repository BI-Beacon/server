TOPTARGETS := all clean setup
SUBDIRS := docs

$(TOPTARGETS): $(SUBDIRS)
$(SUBDIRS):
	which pipenv || pip install pipenv
	pipenv run $(MAKE) -C $@ $(MAKECMDGOALS)

clean:
	rm -f *~

.PHONY: $(TOPTARGETS) $(SUBDIRS)
