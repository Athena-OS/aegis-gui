# install_prefs.py
#
# Copyright 2022
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-only

from aegis_gui.utils import disks
import json


class InstallPrefs:
    def __init__(
        self,
        timezone,
        locale,
        layout,
        variant,
        username,
        shell,
        password,
        enable_sudo,
        disk,
        hostname,
        snapper_enabled,
        zramd_enabled,
        hardened_enabled,
        kernel,
        desktop,
        theme,
        displaymanager,
        browser,
        terminal,
        partition_mode,
        partitions,
    ):
        self.timezone = timezone
        self.locale = locale
        self.layout = layout
        self.variant = variant
        self.username = username
        self.shell = shell
        self.password = password
        self.enable_sudo = enable_sudo
        if partition_mode.lower() != "manual":
            self.disk = disk.disk
        else:
            self.disk = ""
        self.hostname = hostname if len(hostname) != 0 else "athena"
        self.snapper_enabled = snapper_enabled
        self.zramd_enabled = zramd_enabled
        self.hardened_enabled = hardened_enabled
        self.kernel = kernel
        self.desktop = desktop
        self.theme = theme
        self.displaymanager = displaymanager
        self.browser = browser
        self.terminal = terminal
        self.partition_mode = partition_mode
        self.partitions = partitions
        self.is_efi = disks.get_uefi()
        self.bootloader_type = "grub-efi" if self.is_efi else "grub-legacy"
        self.bootloader_location = "/boot/efi/" if self.is_efi else self.disk

    def generate_json(self):
        prefs = {
            "partition": {
                "device": self.disk,
                "mode": self.partition_mode,
                "efi": self.is_efi,
                "partitions": self.partitions,
            },
            "bootloader": {
                "type": self.bootloader_type,
                "location": self.bootloader_location,
            },
            "locale": {
                "locale": self.locale,
                "keymap": self.layout.country_shorthand,
                "timezone": self.timezone.region + "/" + self.timezone.location,
            },
            "networking": {"hostname": self.hostname, "ipv6": False},
            "users": [
                {
                    "name": self.username,
                    "password": self.password,
                    "hasroot": self.enable_sudo,
                    "shell": self.shell.lower(),
                }
            ],
            "rootpass": self.password,
            "desktop": self.desktop.lower(),
            "theme": self.theme.lower(),
            "displaymanager": self.displaymanager.lower(),
            "browser": self.browser.lower(),
            "terminal": self.terminal.lower(),
            "snapper": self.snapper_enabled,
            "extra_packages": ["flameshot"],
            "flatpak": False,
            "zramd": self.zramd_enabled,
            "hardened": self.hardened_enabled,
            "kernel": self.kernel.lower(),
        }
        return json.dumps(prefs)

# Note: if you get error on missing element on json file, the elements required on json file are defined in config.rs of backend