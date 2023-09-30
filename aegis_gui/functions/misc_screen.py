# misc_screen.py

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

from gi.repository import Gtk, Adw
from gettext import gettext as _
from aegis_gui.classes.aegis_screen import AegisScreen


@Gtk.Template(resource_path="/org/athenaos/aegisgui/pages/misc_screen.ui")
class MiscScreen(AegisScreen, Adw.Bin):
    __gtype_name__ = "MiscScreen"

    hostname_entry = Gtk.Template.Child()
    #ipv_switch = Gtk.Template.Child()
    timeshift_switch = Gtk.Template.Child()
    snapper_switch = Gtk.Template.Child()
    zramd_switch = Gtk.Template.Child()
    hardened_switch = Gtk.Template.Child()

    hostname = "athena"
    ipv_enabled = False
    timeshift_enabled = False
    snapper_enabled = True
    zramd_enabled = True
    hardened_enabled = False
    move_to_summary = False

    def __init__(self, window, application, **kwargs):
        super().__init__(**kwargs)
        self.window = window

        self.set_valid(True)

    def on_complete(self, *_):
        self.hostname = self.hostname_entry.get_text()
        #self.ipv_enabled = self.ipv_switch.get_state()
        self.zramd_enabled = self.zramd_switch.get_state()
        self.hardened_enabled = self.hardened_switch.get_state()
        self.timeshift_enabled = self.timeshift_switch.get_state()
        self.snapper_enabled = self.snapper_switch.get_state()
