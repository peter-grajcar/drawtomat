SOURCES = ./src

.PHONY: udpipe install run run-api apidocs

install: venv udpipe conceptualcaptions

udpipe: resources/udpipe

fasttext: resources/fasttext

conceptualcaptions: resources/conceptualcaptions

venv: venv/bin/activate

run: install
	PYTHONPATH=${SOURCES} venv/bin/python3 -m drawtomat

run-api: install
	PYTHONPATH=${SOURCES} FLASK_APP=drawtomat.api.py venv/bin/flask run

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
	wget https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M.vec.zip -O $@/wiki-news-300d-1M.vec.zip
	unzip $@/wiki-news-300d-1M.vec.zip -d $@
	rm -f $@/wiki-news-300d-1M.vec.zip

resources/conceptualcaptions:
	mkdir -p $@
	wget https://www.ms.mff.cuni.cz/~grajcarp/drawtomat/train.wv.model.tar.gz -O $@/train.wv.model.tar.gz
	tar -xzf $@/train.wv.model.tar.gz -C $@
	rm -f $@/train.wv.model.tar.gz

venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate; venv/bin/pip3 install -Ur requirements.txt
	@touch venv/bin/activate

