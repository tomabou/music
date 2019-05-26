import pyaudio
import wave
import sys
import time

CHUNK = 1024

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)


wf = wave.open(sys.argv[1], 'rb')

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)


data = wf.readframes(CHUNK)

c = 0
while True:

    time.sleep(0.015)
    x = time.time()
    stream.write(data)  # blocking
    y = time.time()
    data = wf.readframes(CHUNK)
    z = time.time()
    c += 1
    if c % 40 == 0:
        print("hoge")
        print(x-y)
        print(y-z)

    if data == b'':
        wf.rewind()
        data = wf.readframes(CHUNK)
        print("rewind")

stream.stop_stream()
stream.close()

p.terminate()
