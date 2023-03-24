#!/bin/sh
apt-get update
apt-get install -y iftop dnsutils
cp /vagrant/keyboard /etc/default/keyboard
sudo setupcon