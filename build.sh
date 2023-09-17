#!/usr/bin/env bash
if [[ $1 == "build" ]]; then
	if [[ ! -d "build" ]]; then
		meson build
	else
		meson --reconfigure build
	fi
	ninja -C build
elif [[ $1 == "install" ]]; then
	pushd build
	sudo ninja install
elif [[ $1 == "build-install" ]]; then
	if [[ ! -d "build" ]]; then
		meson build
	else
		meson --reconfigure build
	fi
	ninja -C build
	pushd build
	sudo ninja install
else 
	echo "Unkown command $1"
	echo "usage:"
	echo "build 		build aegis gui"
	echo "install	install aegis gui"
	echo "build-install	build and install aegis_gui"
fi
