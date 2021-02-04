SOURCES                     := ./src
FASTTEXT_MODEL_URL_BASE     := https://www.ms.mff.cuni.cz/~grajcarp/drawtomat
FASTTEXT_MODEL_FILENAME     := conceptual-captions-fasttext.model.tar.gz
SKLEARN_MODEL_URL_BASE		:= https://www.ms.mff.cuni.cz/~grajcarp/drawtomat
SKLEARN_MODEL_FILENAME		:= constraints.model.tar.gz

.PHONY: udpipe fasttext sklearn install run run-api apidocs

install: venv udpipe fasttext sklearn

udpipe: resources/udpipe

fasttext: resources/fasttext

sklearn: resources/sklearn

venv: venv/bin/activate

run: install
	PYTHONPATH=${SOURCES} venv/bin/python3 -m drawtomat

run-api: install
	PYTHONPATH=${SOURCES} FLASK_APP=drawtomat.api.py venv/bin/flask run --host=0.0.0.0

apidocs:
	sphinx-apidoc -o docs/source src -f -e
	$(MAKE) -C docs html

test: install
	PYTHONPATH=./src:./test python3 test/$(TEST).py

resources/udpipe:
	mkdir -p $@
	(cd $@ && curl -O resources/udpipe --remote-name-all https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3131{/english-ewt-ud-2.5-191206.udpipe,/english-partut-ud-2.5-191206.udpipe,/english-lines-ud-2.5-191206.udpipe,/english-gum-ud-2.5-191206.udpipe})
	@touch $@/*

resources/fasttext:
	mkdir -p $@
	wget $(FASTTEXT_MODEL_URL_BASE)/$(FASTTEXT_MODEL_FILENAME) -O $@/$(FASTTEXT_MODEL_FILENAME)
	tar -xzf $@/$(FASTTEXT_MODEL_FILENAME) -C $@
	rm -f $@/$(FASTTEXT_MODEL_FILENAME)

resources/sklearn:
	mkdir -p $@
	wget $(SKLEARN_MODEL_URL_BASE)/$(SKLEARN_MODEL_FILENAME) -O $@/$(SKLEARN_MODEL_FILENAME)
	tar -xzf $@/$(SKLEARN_MODEL_FILENAME) -C $@
	rm -f $@/$(SKLEARN_MODEL_FILENAME)

venv/bin/activate: requirements.txt
	test -d venv || virtualenv -p python3 venv
	. venv/bin/activate; venv/bin/pip3 install -Ur requirements.txt
	@touch venv/bin/activate

