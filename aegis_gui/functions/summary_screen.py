# summary_screen.py

#
# Copyright 2022 user

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

import os
from aegis_gui.utils import disks
from aegis_gui.classes.install_prefs import InstallPrefs
from aegis_gui.utils.threading import RunAsync
from aegis_gui.classes.aegis_screen import AegisScreen
from gi.repository import Gtk, Adw
from gettext import gettext as _


@Gtk.Template(resource_path="/org/athenaos/aegisgui/pages/summary_screen.ui")
class SummaryScreen(AegisScreen, Adw.Bin):
    __gtype_name__ = "SummaryScreen"

    timezone_label = Gtk.Template.Child()
    timezone_button = Gtk.Template.Child()
    locales = Gtk.Template.Child()
    keyboard_label = Gtk.Template.Child()
    keyboard_button = Gtk.Template.Child()
    username_label = Gtk.Template.Child()
    username_button = Gtk.Template.Child()
    shell_label = Gtk.Template.Child()
    shell_button = Gtk.Template.Child()
    sudo_label = Gtk.Template.Child()
    sudo_button = Gtk.Template.Child()
    root_label = Gtk.Template.Child()
    root_button = Gtk.Template.Child()
    desktop_label = Gtk.Template.Child()
    desktop_button = Gtk.Template.Child()
    theme_label = Gtk.Template.Child()
    theme_button = Gtk.Template.Child()
    displaymanager_label = Gtk.Template.Child()
    displaymanager_button = Gtk.Template.Child()
    browser_label = Gtk.Template.Child()
    browser_button = Gtk.Template.Child()
    terminal_label = Gtk.Template.Child()
    terminal_button = Gtk.Template.Child()
    partition_label = Gtk.Template.Child()
    partition_button = Gtk.Template.Child()
    uefi_label = Gtk.Template.Child()
    timeshift_label = Gtk.Template.Child()
    timeshift_button = Gtk.Template.Child()
    snapper_label = Gtk.Template.Child()
    snapper_button = Gtk.Template.Child()
    zramd_label = Gtk.Template.Child()
    zramd_button = Gtk.Template.Child()
    added_locales = []

    def __init__(self, window, application, **kwargs):
        super().__init__(**kwargs)
        self.window = window

        self.set_valid(True)

        self.locale_button = Gtk.Button(
            icon_name="document-edit-symbolic",
            halign="center",
            valign="center"
        )
        self.locales.add_action(self.locale_button)

        self.timezone_button.connect(
            "clicked", self.window.show_page, self.window.timezone_screen
        )
        self.locale_button.connect(
            "clicked", self.window.show_page, self.window.locale_screen
        )
        self.keyboard_button.connect(
            "clicked", self.window.show_page, self.window.keyboard_screen
        )
        self.username_button.connect(
            "clicked", self.window.show_page, self.window.user_screen
        )
        self.shell_button.connect( # In Summary window, when click on edit on Shell row, it comes back to the Shell section to edit your previous choice
            "clicked", self.window.show_page, self.window.shell_screen
        )
        self.sudo_button.connect(
            "clicked", self.window.show_page, self.window.user_screen
        )
        self.root_button.connect(
            "clicked", self.window.show_page, self.window.user_screen
        )
        self.desktop_button.connect(
            "clicked", self.window.show_page, self.window.desktop_screen
        )
        self.theme_button.connect(
            "clicked", self.window.show_page, self.window.theme_screen
        )
        self.displaymanager_button.connect(
            "clicked", self.window.show_page, self.window.displaymanager_screen
        )
        self.browser_button.connect(
            "clicked", self.window.show_page, self.window.browser_screen
        )
        self.terminal_button.connect(
            "clicked", self.window.show_page, self.window.terminal_screen
        )
        self.partition_button.connect(
            "clicked", self.window.show_page, self.window.partition_screen
        )
        self.timeshift_button.connect(
            "clicked", self.window.show_page, self.window.misc_screen
        )
        self.snapper_button.connect(
            "clicked", self.window.show_page, self.window.misc_screen
        )
        self.zramd_button.connect(
            "clicked", self.window.show_page, self.window.misc_screen
        )

    def on_show(self):
        self.timezone_label.set_title(
            self.window.timezone_screen.chosen_timezone.region
            + "/"
            + self.window.timezone_screen.chosen_timezone.location
        )
        for i in self.window.locale_screen.chosen_locales:
            if i not in self.added_locales:
                self.locales.add_row(
                    Adw.ActionRow(
                        title=i,
                        activatable=False,
                        selectable=False,
                        subtitle="Main locale" if i == self.window.locale_screen.chosen_locales[0] else ""
                    )
                )
                self.added_locales.append(i)
        if len(self.window.locale_screen.chosen_locales) >= 5:
            self.locales.set_expanded(False)
        else:
            self.locales.set_expanded(True)

        self.keyboard_label.set_title(self.window.keyboard_screen.variant.country)
        self.keyboard_label.set_subtitle(self.window.keyboard_screen.variant.variant)

        self.username_label.set_title(self.window.user_screen.username)
        self.shell_label.set_title(self.window.shell_screen.chosen_shell+" shell") # In Summary window, it shows the name of the chosen shell. It retrieves the choice from the Shell section window
        self.sudo_label.set_title(
            "sudo enabled" if self.window.user_screen.sudo_enabled else "sudo disabled"
        )
        self.root_label.set_title(
            "root enabled" if self.window.user_screen.root_enabled else "root disabled"
        )

        self.desktop_label.set_title(self.window.desktop_screen.chosen_desktop)

        self.theme_label.set_title(self.window.theme_screen.chosen_theme)

        self.displaymanager_label.set_title(self.window.displaymanager_screen.chosen_displaymanager)

        self.browser_label.set_title(self.window.browser_screen.chosen_browser)

        self.terminal_label.set_title(self.window.terminal_screen.chosen_terminal)

        if self.window.partition_mode == "Manual":
            self.partition_label.set_title("Manual partitioning selected")
            self.partition_label.set_subtitle("")
        else:
            self.partition_label.set_title(
                self.window.partition_screen.selected_partition.disk
            )
            self.partition_label.set_subtitle(
                self.window.partition_screen.selected_partition.disk_size
            )
        self.uefi_label.set_title("UEFI" if disks.get_uefi() else "Legacy BIOS")

        self.timeshift_label.set_title(
            "timeshift enabled"
            if self.window.misc_screen.timeshift_enabled
            else "timeshift disabled"
        )
        self.snapper_label.set_title(
            "snapper enabled"
            if self.window.misc_screen.snapper_enabled
            else "snapper disabled"
        )
        self.zramd_label.set_title(
            "zramd enabled"
            if self.window.misc_screen.zramd_enabled
            else "zramd disabled"
        )

        partitions = []
        for i in range(0, len(self.window.available_partitions)):
            partition = self.window.partition_screen.partition_list.get_row_at_index(
                i
            ).partition
            partitions.append(partition.generate_aegis_entry())

        self.installprefs = InstallPrefs(
            timezone=self.window.timezone_screen.chosen_timezone,
            locale=self.window.locale_screen.chosen_locales,
            layout=self.window.keyboard_screen.variant,
            variant=self.window.keyboard_screen.variant,
            username=self.window.user_screen.username,
            password=self.window.user_screen.password,
            enable_sudo=self.window.user_screen.sudo_enabled,
            disk=self.window.partition_screen.selected_partition,
            hostname=self.window.misc_screen.hostname,
            timeshift_enabled=self.window.misc_screen.timeshift_enabled,
            snapper_enabled=self.window.misc_screen.snapper_enabled,
            zramd_enabled=self.window.misc_screen.zramd_enabled,
            desktop=self.window.desktop_screen.chosen_desktop,
            theme=self.window.theme_screen.chosen_theme,
            displaymanager=self.window.displaymanager_screen.chosen_displaymanager,
            shell=self.window.shell_screen.chosen_shell,
            browser=self.window.browser_screen.chosen_browser,
            terminal=self.window.terminal_screen.chosen_terminal,
            partition_mode=self.window.partition_mode,
            partitions=partitions,
        )
        print(self.installprefs.generate_json())
