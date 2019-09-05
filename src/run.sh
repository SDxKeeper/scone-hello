#!/bin/bash

if [ -d "/conf" ]; then
    export SCONE_FSPF_KEY=$(cat /conf/keytag | awk '{print $11}')
    export SCONE_FSPF_TAG=$(cat /conf/keytag | awk '{print $9}')
    export SCONE_FSPF=/conf/fspf.pb
fi

SCONE_VERSION=1 SCONE_HEAP=2G /home/sample/build/hello_world $@
