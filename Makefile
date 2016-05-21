name = dilbert-tools
package = $(shell ./setup.py --name)
version = $(shell ./setup.py --version)

all: scripts
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

zip_base = dist/${version}/${name}-${version}

do_windows = 0
ifneq "$(wildcard dist/${version}/fetch-dilbert.exe)" ""
 ifneq "$(wildcard dist/${version}/update-dilbert.exe)" ""
  do_windows = 1
 endif
endif

ifneq "${do_windows}" "0"
 windows_zip = ${zip_base}-windows.zip
else
 windows_zip = 
endif

no_windows_warning:
	@[ x"${do_windows}" != x"0" ] && true || \
	echo 'warning: not creating Windows zip file because not all EXEs' \
	     'exist in' "dist/${version}" >&2

dist: sdist ${zip_base}-posix.zip ${windows_zip} no_windows_warning

dist/${version}/${name}-${version}-%.zip: platform = $*
dist/${version}/${name}-${version}-%.zip: in_dir = dist/${version}
dist/${version}/${name}-${version}-%.zip: out_dir = $(dir $@)
dist/${version}/${name}-${version}-%.zip: tmp_dir = ${out_dir}/tmp-zip
dist/${version}/${name}-${version}-%.zip: tmp_file = ${out_dir}/tmp.zip
dist/${version}/${name}-${version}-%.zip: prep scripts
	rm -rf "${tmp_dir}" "${tmp_file}"
	mkdir -p "${tmp_dir}/${name}-${version}-$*"
	@if [ x"${platform}" = x"windows" ]; then \
	 for i in fetch update; do \
	  [ -f "${in_dir}/$$i-dilbert.exe" ] && continue; \
	  echo 'warning: not creating Windows zip file because not all EXEs' \
	       'exist in' "${in_dir}" >&2; \
	  exit; \
	 done; \
	fi
	cd "${in_dir}"; zip -r "../../${tmp_file}" . \
	 -x "*.zip" -x "*.tar.gz" -x "*tmp*"
	zip -r "${tmp_file}" README.md CHANGES.md LICENSE.txt
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
