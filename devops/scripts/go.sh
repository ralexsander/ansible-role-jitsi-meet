#!/bin/bash
#
#

if [ ! -f devops/.venv/bin/activate ]; then virtualenv --no-site-packages devops/.venv; fi
source devops/.venv/bin/activate

cd devops || exit
pip install -U -r requirements.txt > /dev/null

# Install external ansible role dependencies
ansible-galaxy install -r requirements.yml > /dev/null

docker pull msheiny/debian-jessie-systemd:latest

uname -r | grep "grsec" && sudo sysctl -w kernel.grsecurity.chroot_deny_chmod=0

if [ "$1" != "only_tests" ]; then
    molecule create
    molecule converge
fi

#testinfra --connection=docker --hosts=prod tests/
