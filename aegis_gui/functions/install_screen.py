# installer_Screen.py

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

import subprocess, os, shutil
import asyncio
from gi.repository import Gtk, GLib, Adw, Vte, Pango
from gettext import gettext as _
from aegis_gui.utils.command import CommandUtils
from aegis_gui.classes.aegis_screen import AegisScreen
import time


@Gtk.Template(resource_path="/org/athenaos/aegisgui/pages/install_screen.ui")
class InstallScreen(AegisScreen, Adw.Bin):
    __gtype_name__ = "InstallScreen"

    log_box = Gtk.Template.Child()

    def __init__(self, window, application, **kwargs):
        super().__init__(**kwargs)
        self.window = window

        # Vte instance
        self.vte_instance = Vte.Terminal()
        self.vte_instance.set_cursor_blink_mode(Vte.CursorBlinkMode.ON)
        self.vte_instance.set_mouse_autohide(True)
        self.vte_instance.set_font(Pango.FontDescription("Source Code Pro Regular 12"))
        self.log_box.append(self.vte_instance)
        self.vte_instance.connect("child-exited", self.on_vte_child_exited)

        self.set_valid(False)

    def on_show(self):
        prefs = self.window.summary_screen.installprefs.generate_json()
        with open(os.getenv("HOME") + "/.config/aegis.json", "w") as f:
            f.write(prefs)

        prefs = self.window.summary_screen.installprefs.generate_json()

        log_file_path = "/tmp/aegis-gui-output.txt"
        log_file = open(log_file_path, "a")  # Open the log file in append mode

        self.vte_instance.spawn_async(
            Vte.PtyFlags.DEFAULT,
            ".",  # working directory
            ["bash", "-c", f"cat /usr/share/aegis-gui/aegis_gui/scripts/install.sh | bash -s 2>&1 | tee -a {log_file_path}"], # using cat to read the content of the install.sh script and then piping it into bash with the -s option. This allows you to run the script without marking it as executable. By the way, this line is used to redirect stdout and stderr to both GTK window and output log file
            [],  # environment
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
            -1,
            None,
            None,
        )
        log_file.close()

    def on_vte_child_exited(self, *args):
        self.set_valid(True)
