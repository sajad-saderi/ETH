# Vagrant

First, install `vagrant` according to your distro:

E.g.:
```
pacman -S vagrant
```

To run this VM, execute

```
vagrant up
```

in this directory.

You can SSH into the VM with

```
vagrant ssh
```

Username: `vagrant`  
Password: `vagrant`

Shut the VM down with:

```
vagrant halt
```

For a clean start, destroy the VM and then `up` it again:

```
vagrant destroy
vagrant up
```