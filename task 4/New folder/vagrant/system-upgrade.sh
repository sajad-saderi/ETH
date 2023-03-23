#!/bin/sh
export DEBIAN_FRONTEND=noninteractive
apt-mark hold linux-image-amd64  # kernel upgrade breaks VirtualBox drivers
apt-mark hold grub-pc  # grub update fails due to this being a Vagrant box
apt-get update
apt-get dist-upgrade -y