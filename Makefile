name = dilbert-tools
package := $(shell ./setup.py --name)
version := $(shell ./setup.py --version)

src_dir = ${package}

all: scripts
.PHONY: scripts dist sdist zips prep clean

define prep =
 mkdir -p "dist/${version}"
endef

scripts: dist/${version}/fetch-dilbert \
         dist/${version}/update-dilbert

dist/${version}/%-dilbert: tmp_dir = dist/${version}/tmp-$*
dist/${version}/%-dilbert: zip = ${tmp_dir}/$*.zip
dist/${version}/%-dilbert: main_py = ${tmp_dir}/__main__.py
dist/${version}/%-dilbert: ${src_dir}/* Makefile
	$(prep)
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

dist: sdist zips

sdist: dist/${version}/${package}-${version}.tar.gz

dist/${version}/${package}-${version}.tar.gz: ${src_dir}/* Makefile
	$(prep)
	./setup.py sdist
	mv "dist/${package}-${version}.tar.gz" "dist/${version}"

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

define no_windows_warning =
	[ x"${do_windows}" != x"0" ] && true || \
	echo 'warning: not creating Windows zip file because not all EXEs' \
	     'exist in' "dist/${version}" >&2
endef

$(shell $(no_windows_warning))

zips: ${zip_base}-posix.zip ${windows_zip}

dist/${version}/${name}-${version}-%.zip: platform = $*
dist/${version}/${name}-${version}-%.zip: out_dir = $(dir $@)
dist/${version}/${name}-${version}-%.zip: tmp_dir = ${out_dir}/tmp-zip
dist/${version}/${name}-${version}-%.zip: tmp_file = ${tmp_dir}/tmp.zip
dist/${version}/${name}-${version}-%.zip: src = dist/${version}
dist/${version}/${name}-${version}-%.zip: dest = ${tmp_dir}/${name}-${version}-$*
dist/${version}/${name}-${version}-%.zip: ${src_dir}/* Makefile | scripts
	$(prep)
	rm -rf "${tmp_dir}" "${tmp_file}"
	mkdir -p "${dest}"
	cp -a README.md CHANGES.md LICENSE.txt "${dest}"
	for i in fetch update; do \
	 cp -a "${src}/$$i-dilbert" "${dest}"; \
	 if [ x"${platform}" = x"windows" ]; then \
	  cp -a "${src}/$$i-dilbert.exe" "${dest}"; \
	  mv "${dest}/$$i-dilbert" "${dest}/$$i-dilbert.py"; \
	 fi; \
	done
	if [ x"${platform}" = x"windows" ]; then \
	 for i in CHANGES README; do \
	  if [ -f "${dest}/$$i.md" ]; then \
	   sed -e 's/\r\?$$/\r/g' < "${dest}/$$i.md" > "${dest}/$$i.txt"; \
	   rm -f "${dest}/$$i.md"; \
	  fi; \
	 done; \
	fi
	cd "${tmp_dir}"; zip -r "$(notdir ${tmp_file})" "$(notdir ${dest})"
	mv "${tmp_file}" "$@"
	rm -rf "${tmp_dir}"
	@$(no_windows_warning)

prep:
	mkdir -p "dist/${version}"

clean:
	rm -rf dist/*
