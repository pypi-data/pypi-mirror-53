'''
Presets for configuration file
'''

from ..version import __version__ as version

__all__ = 'DEFAULT', 'OVERWRITE'


DEFAULT = {
    'gui': ('gui-tkinter', str),
    'icon_size': ('1.0', float),
    'map_size': ('1.0', float),
    'autosave': ('autosave.json', str),
    'button_layout': ('buttons.json', str),
    'window_layout': ('windows.json', str),

    'entrance_randomiser': (True, bool),
    'world_state': ('Open', str),
    'glitch_mode': ('None', str),
    'item_placement': ('Advanced', str),
    'dungeon_items': ('Standard', str),
    'goal': ('Defeat Ganon', str),
    'swords': ('Randomised', str),
}


OVERWRITE = {
    '0.9.0': set(),
    '0.9.1': set(),
    '0.9.2': set(),
}
