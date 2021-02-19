#!/bin/sh

# This is the client that staff uses to file new issues.

echo -n "Server [localhost]: "
read server
if [ -z "$server" -a "$server" != " " ]; then
  server="localhost"
fi
echo -n "Port [3333]: "
read port
if [ -z "$port" -a "$port" != " " ]; then
  port=4321
fi
echo -n "Enter your name: "
read name
echo -n "Summarize your issue in few words: "
read subject
echo -n "Describe your issue in detail: "
read description
echo -n "Enter the path of a picture (PNG) you want to attach (e.g. a screenshot that shows the problem): "
read filename

image=$(cat $filename | base64 | tr -d '\n')

curl -X POST -H "Content-Type: application/json" -d "{\"author\": \"$name\", \"subject\": \"$subject\", \"description\": \"$description\", \"image\": \"$image\"}" http://${server}:${port}/issue
