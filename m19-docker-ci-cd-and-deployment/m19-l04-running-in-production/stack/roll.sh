#!/bin/sh
# usage: ./roll.sh 2   (roll every app container to version 2)
set -e
export V1=$1 V2=$1
for app in app1 app2; do
  sed -i.bak "/# $app/s/;/ down;/" conf/default.conf
  docker exec m19l04-proxy nginx -s reload
  docker compose up -d --wait --force-recreate $app
  sed -i.bak "/# $app/s/ down;/;/" conf/default.conf
  docker exec m19l04-proxy nginx -s reload
done
