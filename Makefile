package = $(shell ./setup.py --name)
version = $(shell ./setup.py --version)

all: dist/fetch-dilbert-${version} dist/update-dilbert-${version} sdist
.PHONY: sdist prep clean

src_dir = ${package}

dist/%-dilbert-${version}: tmp_dir = dist/tmp-$*
dist/%-dilbert-${version}: zip = ${tmp_dir}/$*.zip
dist/%-dilbert-${version}: main_py = ${tmp_dir}/__main__.py
dist/%-dilbert-${version}: prep
	rm -rf "${tmp_dir}"
	mkdir -p "${tmp_dir}"
	zip -r "${zip}" "${src_dir}"/*.py
	cp -a __main__.py.in "${main_py}"
	sed -i -e 's/___PACKAGE___/${package}/g' "${main_py}"
	sed -i -e 's/___MODULE___/$*/g' "${main_py}"
	zip --junk-paths "${zip}" "${main_py}"
	echo '#!/usr/bin/env python2' > "$@"
	cat "${zip}" >> "$@"
	chmod a+x "$@"
	rm -rf "${tmp_dir}"

sdist:
	./setup.py sdist

prep:
	mkdir -p dist

clean:
	rm -rf dist/*
