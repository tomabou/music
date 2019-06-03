import pyaudio
import wave
import sys
import time
from lib.MusicData import SONGS, Chord
import lib.Flags as Flags
import math
import lib.Flags as Flags
import threading


CHORD = Chord('D', 0)
CHUNK = 1024
IS_RUN = True
SONG_NUM = 1


def get_chord(song_num, song_ratio):
    song_list = SONGS[song_num]
    l = len(song_list)
    index = int(song_ratio * l)
    index = min(l - 1, max(0, index))
    return song_list[index]


def set_global_chord(song_num, song_ratio):
    c = get_chord(song_num, song_ratio)
    global CHORD
    if CHORD != c:
        CHORD = c
        print("set chord {}".format(song_ratio))


def get_filepath(i):
    return "./files/song" + str(i) + ".wav"


def play_music():
    wfs = []
    frame_lengths = []
    now_song = SONG_NUM
    for i in range(2):
        wfs.append(wave.open(get_filepath(i), 'rb'))
        frame_lengths.append(wfs[i].getnframes())

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wfs[0].getsampwidth()),
                    channels=wfs[0].getnchannels(),
                    rate=wfs[0].getframerate(),
                    output=True)

    data = wfs[now_song].readframes(CHUNK)

    now_frame = 0
    while not Flags.FINISH:
        stream.write(data)  # blocking
        now_frame += CHUNK
        data = wfs[now_song].readframes(CHUNK)
        song_ratio = now_frame / float(frame_lengths[now_song])

        set_global_chord(now_song, song_ratio)
        if data == b'':
            now_song = SONG_NUM
            wfs[now_song].rewind()
            now_frame = 0
            data = wfs[now_song].readframes(CHUNK)
            print("rewind")

    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == '__main__':
    t = threading.Thread(target=play_music)
    t.start()
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        # all note off
        Flags.FINISH = True
