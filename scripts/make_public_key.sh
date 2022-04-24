#!/bin/sh

openssl pkcs8 -nocrypt -in store_key.p8 -out store_key_public.pem
