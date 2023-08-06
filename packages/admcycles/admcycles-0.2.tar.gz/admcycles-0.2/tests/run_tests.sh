#/usr/bin/env bash

if [ -z ${SAGE+x} ]
then
    SAGE=sage
fi

cd "${0%/*}"
${SAGE} automorphism_groups.py
