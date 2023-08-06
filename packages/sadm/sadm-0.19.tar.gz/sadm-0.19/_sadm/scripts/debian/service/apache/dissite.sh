#!/bin/sh -eu
for s in $@; do
	if a2query -q -s ${s}; then
		a2dissite ${s}
	fi
done
exit $?
