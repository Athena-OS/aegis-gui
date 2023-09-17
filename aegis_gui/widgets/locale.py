# timezone.py

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

from datetime import datetime
import pytz
from gi.repository import Gtk, GLib, Adw
from gettext import gettext as _
from pytz import timezone


@Gtk.Template(resource_path="/org/athenaos/aegisgui/widgets/locale.ui")
class LocaleEntry(Adw.ActionRow):
    __gtype_name__ = "LocaleEntry"

    main_locale_button = Gtk.Template.Child()

    def __init__(self, page, window, locale, button_group, application, **kwargs):
        super().__init__(**kwargs)

        self.window = window
        self.page = page
        self.locale = locale

        self.set_title(locale)
        if button_group is not None:
            self.main_locale_button.set_group(button_group)
        self.main_locale_button.connect("toggled", self.set_as_main_locale)

    def set_as_main_locale(self, button):
        self.page.main_locale = self.locale

    def get_timezone(self):
        return timezone(str(self))
