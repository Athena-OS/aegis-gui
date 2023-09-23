pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
widgetsdir = join_paths(pkgdatadir, 'aegis_gui/widgets')

aegis_gui_sources = [
    '__init__.py',
    'timezone.py',
    'layout.py',
    'variant.py',
    'desktop.py',
    'theme.py',
    'displaymanager.py',
    'shell.py',
    'browser.py',
    'terminal.py',
    'disk.py',
    'partition.py',
    'locale.py',
    'selected_locale.py',
]
install_data(aegis_gui_sources, install_dir: widgetsdir)
