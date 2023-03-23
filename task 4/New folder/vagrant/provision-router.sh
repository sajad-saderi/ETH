#!/bin/sh
echo 'net.ipv4.ip_forward = 1' > /etc/sysctl.d/ip_forward.conf
sysctl -p /etc/sysctl.d/ip_forward.conf
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
export DEBIAN_FRONTEND=noninteractive
apt-get install -y iptables-persistent dnsutils
cp /vagrant/keyboard /etc/default/keyboard
sudo setupcon