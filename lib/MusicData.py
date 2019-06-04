from types import *


class Chord(object):
    quality_list = [
        '',
        'm',
        '7',
        'm7',
        'M7',
        'mM7',
        'dim',
    ]
    root_list = ['C', 'C#', 'D', 'D#', 'E',
                 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    func_list = ['1', '1#', '2', '2#', '3',
                 '4', '4#', '5', '5#', '6', '6#', '7']

    "function is mode"

    def __init__(self, root, quality, func=None, ratio=0.5):
        if isinstance(root, IntType):
            self.root = root
        else:
            self.root = self.root_list.index(root)

        if isinstance(quality, IntType):
            self.quality = quality
        else:
            self.quality = self.quality_list.index(quality)

        if func is not None:
            self.function = func
        else:
            self.function = self.root

        self.ratio = ratio

    def __str__(self):
        q = self.quality_list[self.quality]
        return self.root_list[self.root] + q + \
            " " + self.func_list[self.function] + q

    def __eq__(self, other):
        return self.root == other.root \
            and self.quality == other.quality \
            and self.function == self.function

    def __ne__(self, other):
        return not self.__eq__(other)


small_ratio = 0.4

SONGS = [[
    Chord('A', 'm'),
    Chord('A', 'm'),
    Chord('F', ''),
    Chord('F', ''),
    Chord('G', '7'),
    Chord('G', '7'),
    Chord('C', ''),
    Chord('C', ''),
    Chord('A', 'm'),
    Chord('A', 'm'),
    Chord('F', ''),
    Chord('F', ''),
    Chord('G', '7'),
    Chord('G', '7'),
    Chord('C', ''),
    Chord('G', ''),
],
    [
    Chord('C', '', ratio=small_ratio),
    Chord('G', '', ratio=small_ratio),
    Chord('A', 'm', ratio=small_ratio),
    Chord('E', 'm', ratio=small_ratio),
    Chord('F', '', ratio=small_ratio),
    Chord('C', '', ratio=small_ratio),
    Chord('F', '', ratio=small_ratio),
    Chord('G', '7', ratio=small_ratio),
], [
    Chord('A', 'm', ratio=0.0),
    Chord('A', 'm', ratio=0.0),
    Chord('F', '', ratio=0.0),
    Chord('F', '', ratio=0.0),
    Chord('G', '7', ratio=0.0),
    Chord('G', '7', ratio=0.0),
    Chord('C', '', ratio=0.0),
    Chord('C', '', ratio=0.0),
    Chord('C', '', ratio=0.0),
    Chord('C', '', ratio=0.0),
]]
