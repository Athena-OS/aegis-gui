#!/usr/bin/bash
echo "Running reflector to sort for fastest mirrors" | tee -a /tmp/aegis-gui-output.txt
pkexec reflector --latest 5 --sort rate --save /etc/pacman.d/mirrorlist | tee -a /tmp/aegis-gui-output.txt
pkexec athena-aegis config ~/.config/aegis.json | tee -a /tmp/aegis-gui-output.txt
