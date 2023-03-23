#!/bin/sh
apt-get install -y unbound dnsutils
cp /vagrant/unbound-lab.conf /etc/unbound/unbound.conf.d/
rm /etc/unbound/unbound.conf.d/qname-minimisation.conf
systemctl restart unbound
cp /vagrant/keyboard /etc/default/keyboard
sudo setupcon