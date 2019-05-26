from lib.MusicData import Chord


class NoteGenerator(object):
    scale = [0, 2, 4, 5, 7, 9, 11]
    # see Chord.quality
    quality2tone = [
        [0, 4, 7],
        [0, 3, 7],
        [0, 4, 7, 10],
        [0, 3, 7, 10],
        [0, 4, 7, 11],
        [0, 3, 7, 11],
        [0, 3, 6]
    ]

    def __init__(self, min_note, max_note):
        self.min_note = min_note
        self.max_note = max_note
        self.chord = Chord('C', '')

    def gen_tone_list(self):
        tone = []
        for n in self.quality2tone[self.chord.quality]:
            tone.append((n+self.chord.root) % 12)

        return tone


if __name__ == '__main__':
    test = NoteGenerator(50, 70)
    x = test.gen_tone_list()
    print(x)
