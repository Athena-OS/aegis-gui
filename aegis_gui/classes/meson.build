pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
classesdir = join_paths(pkgdatadir, 'aegis_gui/classes')

aegis_gui_sources = [
    '__init__.py',
    'locale.py',
    'keymap.py',
    'install_prefs.py',
    'partition.py',
    'aegis_screen.py'
]
install_data(aegis_gui_sources, install_dir: classesdir)
