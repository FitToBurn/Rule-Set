#!/bin/bash
systemctl stop firewalld
systemctl disable firewalld
echo "1"