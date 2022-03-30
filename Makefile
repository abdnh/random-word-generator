.PHONY: all format clean zip ankiweb run

all: ankiweb zip

zip:
	python -m ankibuild --type package --install --qt all

ankiweb:
	python -m ankibuild --type ankiweb --install --qt all

run: zip
	python -m ankirun

format:
	python -m black src

clean:
	rm -rf build/
