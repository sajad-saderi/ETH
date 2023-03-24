#!/bin/sh
apt-get install -y bundler git nsd dnsutils
apt-get install -y --no-install-recommends python3-scapy
cp /vagrant/nsd-lab.conf /etc/nsd/nsd.conf.d/
cp /vagrant/attacker.sss-wue.de.zone /etc/nsd/
systemctl restart nsd
cd /home/vagrant
git clone https://github.com/iagox86/dnscat2.git
cd dnscat2/server
cp /vagrant/template.py /home/
cp /vagrant/keyboard /etc/default/keyboard
sudo setupcon
bundle install