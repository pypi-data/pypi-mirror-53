#!/bin/sh -eu
if which git >/dev/null; then
	check-manifest
fi
python3 setup.py check
python3 setup.py egg_info
pytest $@
exit 0
