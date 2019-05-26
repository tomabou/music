import lib.Leap as Leap
import sys
import time
import random
import rtmidi
from concurrent.futures import ThreadPoolExecutor
import threading
import lib.Flags as Flags
from lib.NoteGenerator import NoteGenerator
from lib.MusicPlayer import play_music, CHORD


midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print available_ports
use_midi_port_num = int(raw_input())
midiout.open_port(use_midi_port_num)


def note_on(channel, pitch, velo):
    return [0x90+channel, pitch, velo]


def note_off(channel, pitch):
    return [0x80+channel, pitch, 64]


def playnote(note):
    midiout.send_message(note_on(0, note, 112))
    time.sleep(0.5)
    midiout.send_message(note_off(0, note))


class SampleListener(Leap.Listener):
    pre_y_speed = [1, 2]
    pre_note = [60, 60]

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        isDead = [True, True]
        for hand in frame.hands:

            handType = 0 if hand.is_left else 1
            isDead[handType] = False

            y_speed = hand.palm_velocity[1]
            x_pos = hand.palm_position[0]

            note = 72 + nearest_note(int(x_pos) // 20)

            if self.pre_y_speed[handType] > -200 and y_speed <= -200:
                if self.pre_note[handType] != None:
                    midiout.send_message(
                        note_off(0, self.pre_note[handType]))
                midiout.send_message(note_on(0, note, 64))
                self.pre_note[handType] = note
                print "note on %d " % y_speed

            self.pre_y_speed[handType] = y_speed

            print y_speed

        for i, state in enumerate(isDead):
            if state:
                if self.pre_note[i]:
                    midiout.send_message(
                        note_off(0, self.pre_note[i]))
                self.pre_note[i] = None


def nearest_note(x):
    for i in range(3):
        if (x+i) % 12 in [0, 2, 4,  7, 9]:
            return (x + i)


def main():
    playnote(60)

    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        # all note off
        midiout.send_message([0xB0, 123, 0])
        controller.remove_listener(listener)


def test_midi():
    note_generator = NoteGenerator(60, 90)
    for i in range(16):
        if Flags.FINISH:
            return
        n = note_generator.create_tone_note(random.random())
        playnote(n)


def test():
    t1 = threading.Thread(target=test_midi)
    t2 = threading.Thread(target=play_music)
    print("thread created")
    time.sleep(1)
    t1.start()
    t2.start()

    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        # all note off
        Flags.FINISH = True
        midiout.send_message([0xB0, 123, 0])


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test()
    else:
        main()
