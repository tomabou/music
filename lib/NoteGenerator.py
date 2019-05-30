from lib.MusicData import Chord
import random


class NoteGenerator(object):
    scale = [0, 2, 4, 5, 7, 9, 11]
    # see Chord.quality
    quality2note = [
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

    def set_chord(self, c):
        self.chord = c

    def tone_note_list(self):
        note = []
        for n in self.quality2note[self.chord.quality]:
            note.append((n+self.chord.root) % 12)

        note.sort()
        return note

    def avoid_note_list(self):
        note = []
        for n in self.tone_note_list():
            note.append((n+1) % 12)
        note.sort()
        return note

    def scale_note_list(self):
        notes = []
        for n in self.scale:
            note = n + self.chord.root - self.chord.function
            notes.append(note % 12)
        notes.sort()
        return notes

    def available_note_list(self):
        avoid = self.avoid_note_list()
        notes = []
        for n in self.scale_note_list():
            if n not in avoid:
                notes.append(n)
        notes.sort()
        return notes

    def create_note_mix(self, val, latio):
        if latio > random.random():
            return self.create_available_note(val)
        else:
            return self.create_tone_note(val)

    # min~max is correspond to 0.0 ~ 1.0
    # latio : non tone note correction
    def create_available_note(self, val):
        notes = self.available_note_list()
        l = len(notes)
        position = (self.max_note - self.min_note) * val + self.min_note
        position /= 12.0
        oc = int(position)
        note = oc * 12 + notes[int((position-oc)*l)]
        return note

    def create_tone_note(self, val):
        notes = self.tone_note_list()
        l = len(notes)
        position = (self.max_note - self.min_note) * val + self.min_note
        position /= 12.0
        oc = int(position)
        note = oc * 12 + notes[int((position-oc)*l)]
        return note


if __name__ == '__main__':
    test = NoteGenerator(50, 70)
    print(test.chord)
    print(test.scale_note_list())
    print(test.tone_note_list())
    print(test.available_note_list())
    print(test.avoid_note_list())
    test.set_chord(Chord('D', '', 0))
    print(test.chord)
    print(test.scale_note_list())
    print(test.tone_note_list())
    print(test.available_note_list())
    print(test.avoid_note_list())

    for _ in range(10):
        n = test.create_scale_note(random.random())
        print(n)
