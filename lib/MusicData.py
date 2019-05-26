
from types import *


class Chord(object):
    quality_list = [
        '',
        'm',
        '7',
        'm7',
        'M7',
        'mM7'
    ]
    root_list = ['C', 'C#', 'D', 'D#', 'E',
                 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def __init__(self, root, quality):
        if type(root) == IntType:
            self.root = root
        else:
            self.root = self.root_list.index(root)

        if type(quality) == IntType:
            self.quality = quality
        else:
            self.quality = self.quality_list.index(quality)

    def __str__(self):
        return self.root_list[self.root] + self.quality_list[self.quality]


SONGS = [[
    Chord('A', 'm'),
    Chord('A', 'm'),
    Chord('F', ''),
    Chord('F', ''),
    Chord('G', ''),
    Chord('G', ''),
    Chord('C', ''),
    Chord('C', ''),
    Chord('A', 'm'),
    Chord('A', 'm'),
    Chord('F', ''),
    Chord('F', ''),
    Chord('G', ''),
    Chord('G', ''),
    Chord('C', ''),
    Chord('G', ''),
]]
