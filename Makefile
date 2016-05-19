name = dilbert-tools
package = $(shell ./setup.py --name)
version = $(shell ./setup.py --version)

all: scripts sdist dist
.PHONY: scripts sdist dist prep clean

src_dir = ${package}

scripts: dist/${version}/fetch-dilbert \
         dist/${version}/update-dilbert

dist/${version}/%-dilbert: tmp_dir = dist/${version}/tmp-$*
dist/${version}/%-dilbert: zip = ${tmp_dir}/$*.zip
dist/${version}/%-dilbert: main_py = ${tmp_dir}/__main__.py
dist/${version}/%-dilbert: prep
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

sdist: prep
	./setup.py sdist
	mv dist/"$$("./setup.py" --fullname)".tar.gz "dist/${version}"

dist: dist/${version}/${name}-${version}-posix.zip \
      dist/${version}/${name}-${version}-windows.zip

dist/${version}/${name}-${version}-%.zip: platform = $*
dist/${version}/${name}-${version}-%.zip: in_dir = dist/${version}
dist/${version}/${name}-${version}-%.zip: out_dir = $(dir $@)
dist/${version}/${name}-${version}-%.zip: tmp_dir = ${out_dir}/tmp-zip
dist/${version}/${name}-${version}-%.zip: tmp_file = ${out_dir}/tmp.zip
dist/${version}/${name}-${version}-%.zip: prep
	rm -rf "${tmp_dir}" "${tmp_file}"
	mkdir -p "${tmp_dir}/${name}-${version}-$*"
	cd "${in_dir}"; zip -r "../../${tmp_file}" . \
	 -x "*.zip" -x "*.tar.gz" -x "*tmp*"
	zip -r "${tmp_file}" README.md CHANGES.txt LICENSE.txt
	cd "${tmp_dir}/${name}-${version}-$*"; \
	 unzip "../../../../${tmp_file}"; \
	 if [ x"${platform}" = x"posix" ]; then \
	  rm -f *pyi* *.exe; \
	 elif [ x"${platform}" = x"windows" ]; then \
	  for i in fetch update; do \
	   rm -f "$$i-dilbert-pyi"; \
	   mv "$$i-dilbert" "$$i-dilbert.py"; \
	  done; \
	 fi; \
	 for i in CHANGES README; do \
	  if [ -f "$$i.md" ]; then \
	   sed -e 's/\r\?$$/\r/g' < "$$i.md" > "$$i.txt"; \
	   rm -f "$$i.md"; \
	  fi; \
	 done; \
	 cd ..; \
	  rm -f "../../../${tmp_file}"; \
	  zip -r "../../../${tmp_file}" "${name}-${version}-$*"
	rm -rf "${tmp_dir}"
	mv "${tmp_file}" "$@"

prep:
	mkdir -p "dist/${version}"

clean:
	rm -rf dist/*
