#!/bin/sh -ex

tmpdir=$(mktemp -d)

(cd $tmpdir
 sudo openssl req -newkey rsa:4096 -nodes -sha256 \
      -subj "/C=IL/ST=Tel Aviv/L=Tel Aviv/O=Personal/OU=Personal/CN=private-repository-k8s" \
      -keyout ./registry.key -x509 -days 3650 -out ./registry.crt &&
     base64 ./registry.key &&
     echo &&
     base64 ./registry.crt
)
rm -rf $tmpdir
