apidocs:
	sphinx-apidoc -o docs/source drawtomat -f -e
	$(MAKE) -C docs html

udpipe:
	@mkdir -p resources/udpipe
	(cd resources/udpipe && curl -O resources/udpipe --remote-name-all https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3131{/english-ewt-ud-2.5-191206.udpipe,/english-partut-ud-2.5-191206.udpipe,/english-lines-ud-2.5-191206.udpipe,/english-gum-ud-2.5-191206.udpipe})

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate; pip install -Ur requirements.txt
	touch venv/bin/activate

run: venv
	venv/bin/python3 -m drawtomat
