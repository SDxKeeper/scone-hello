FROM sconecuratedimages/crosscompilers:alpine3.7 as build

WORKDIR /home


RUN apk update \
	&& apk add git \
	nasm \
	yasm \
	libdrm

RUN apk update && apk add cmake make libusb-dev boost-dev gtk+2.0-dev

COPY src /home/sample

RUN cd sample && mkdir build && cd build \
    && cmake .. \
    && make -j

FROM iexechub/python-scone as runtime

RUN echo "http://dl-cdn.alpinelinux.org/alpine/v3.5/community" >> /etc/apk/repositories \
    && apk update \
    && apk add --update-cache --no-cache libgcc \
    && apk --no-cache --update-cache add gcc gfortran python python-dev py-pip build-base wget freetype-dev libpng-dev \
    && apk add --no-cache --virtual .build-deps gcc musl-dev


RUN SCONE_MODE=sim pip install attrdict python-gnupg web3

RUN cp /usr/bin/python3.6 /usr/bin/python3

COPY --from=build /home/sample /home/sample

COPY --from=build /opt/scone/cross-compiler/x86_64-linux-musl/lib /opt/scone/cross-compiler/x86_64-linux-musl/lib

COPY signer /signer

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/scone/cross-compiler/x86_64-linux-musl/lib/


RUN SCONE_MODE=sim SCONE_HASH=1 SCONE_HEAP=1G SCONE_ALPINE=1		    \
	&& mkdir /conf							                            \
    && cd /conf                                                         \
	&& scone fspf create fspf.pb 					                    \
	&& scone fspf addr fspf.pb /  --not-protected --kernel /            \
    && scone fspf addr fspf.pb /signer --authenticated --kernel /signer \
	&& scone fspf addr fspf.pb /usr/lib --authenticated --kernel /usr/lib       \
	&& scone fspf addf fspf.pb /usr/lib /usr/lib 			            \
	&& scone fspf addr fspf.pb /bin --authenticated --kernel /bin       \
	&& scone fspf addf fspf.pb /bin /bin 			                    \
	&& scone fspf addr fspf.pb /lib --authenticated --kernel /lib       \
	&& scone fspf addf fspf.pb /lib /lib 			                    \
	&& scone fspf addr fspf.pb /etc --authenticated --kernel /etc       \
	&& scone fspf addf fspf.pb /etc /etc 			                    \
	&& scone fspf addr fspf.pb /sbin --authenticated --kernel /sbin     \
	&& scone fspf addf fspf.pb /sbin /sbin 			                    \
	&& scone fspf addf fspf.pb /signer /signer 			                \
	&& scone fspf encrypt /conf/fspf.pb > /conf/keytag 			        \
	&& MRENCLAVE="$(SCONE_HASH=1 /home/sample/build/hello_world)"			            \
	&& FSPF_TAG=$(cat /conf/keytag | awk '{print $9}') 	                \
	&& FSPF_KEY=$(cat /conf/keytag | awk '{print $11}')		            \
	&& FINGERPRINT="$FSPF_KEY|$FSPF_TAG|$MRENCLAVE"			            \
	&& echo $FINGERPRINT > /conf/fingerprint.txt			            \
	&& printf "\n########################################################\nMREnclave: $FINGERPRINT\n########################################################\n\n"

ENTRYPOINT ["/home/sample/run.sh"] 