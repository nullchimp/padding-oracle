#!/bin/bash

docker kill nullchimp-padorac
docker build -t nullchimp/padding-oracle .
docker run --rm --name nullchimp-padorac -v /home/tvg/Projects/padding-oracle/src:/app/ nullchimp/padding-oracle bash -c 'while true; do sleep 3600; done'