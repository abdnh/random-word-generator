.PHONY: all forms build format clean addon zip

all: build

forms: src/dialog.py

src/dialog.py: designer/dialog.ui 
	pyuic5 $^ > $@

build: forms

format:
	python -m black src

zip: build.zip

build.zip: src/*
	rm -f $@
	rm -f src/meta.json
	rm -rf src/__pycache__
	( cd src/; zip -r ../$@ * )

addon: zip
	cp build.zip random-word-generator.ankiaddon
	cp -r src/* ankiprofile/addons21/random-word-generator

clean:
	rm -f *.pyc
	rm -f src/*.pyc
	rm -f src/__pycache__
	rm -f src/dialog.py
	rm -f build.zip
	rm -f random-word-generator.ankiaddon
