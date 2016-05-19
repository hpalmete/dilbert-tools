package = $(shell ./setup.py --name)
version = $(shell ./setup.py --version)

all: dist/${version}/fetch-dilbert dist/${version}/update-dilbert sdist
.PHONY: sdist prep clean

src_dir = ${package}

dist/${version}/%-dilbert: tmp_dir = dist/${version}/tmp-$*
dist/${version}/%-dilbert: zip = ${tmp_dir}/$*.zip
dist/${version}/%-dilbert: main_py = ${tmp_dir}/__main__.py
dist/${version}/%-dilbert: prep
	mkdir -p "$(dir $@)"
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
	mkdir -p "dist/${version}"
	./setup.py sdist
	mv dist/"$$("./setup.py" --fullname)".tar.gz "dist/${version}"

prep:
	mkdir -p dist

clean:
	rm -rf dist/*
