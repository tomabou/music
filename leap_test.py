import lib.Leap as Leap
import sys
import time
import random
import rtmidi
from concurrent.futures import ThreadPoolExecutor
import threading
import lib.Flags as Flags
from lib.NoteGenerator import NoteGenerator
from lib.MusicPlayer import play_music
import lib.MusicPlayer


midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print available_ports
use_midi_port_num = int(raw_input())
midiout.open_port(use_midi_port_num)

note_generator = NoteGenerator(60, 90)


def note_on(channel, pitch, velo):
    return [0x90+channel, pitch, velo]


def note_off(channel, pitch):
    return [0x80+channel, pitch, 64]


def playnote(note):
    midiout.send_message(note_on(0, note, 112))
    time.sleep(0.5)
    midiout.send_message(note_off(0, note))


class SampleListener(Leap.Listener):

    def on_init(self, controller):
        print "Initialized"
        self.pre_y_speed = [0 for i in range(101)]
        self.pre_tip_y_speed = [0 for i in range(101)]

        self.pre_note = [60, 60]
        self.note_lock = [0, 0]

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def send_note_midi(self, note_num, handType, velo):
        if self.note_lock[handType] > 0:
            return
        if self.pre_note[handType] != None:
            midiout.send_message(
                note_off(handType, self.pre_note[handType]))
        midiout.send_message(note_on(handType, note_num, velo))
        self.note_lock[handType] = 3
        self.pre_note[handType] = note_num
        print(note_num)

    def finger_func(self, finger, handType):
        tip_y_speed = finger.tip_velocity[1]
        tip_x_pos = (finger.tip_position[0] + 200.0)/400.0
        velo = min(127, int(finger.tip_position[1] * 0.18))
        finger_id = finger.id % 100

        if self.pre_tip_y_speed[finger_id] > -400\
                and tip_y_speed <= -400:

            #print("finger in")
            note_generator.set_chord(lib.MusicPlayer.CHORD)
            note = note_generator.create_available_note(tip_x_pos)
            #self.send_note_midi(note, handType, velo)

        self.pre_tip_y_speed[finger_id] = tip_y_speed

    def hand_func(self, hand):
        handType = 0 if hand.is_left else 1

        y_speed = hand.palm_velocity[1]
        x_pos = (hand.palm_position[0] + 200.0)/400.0
        velo = min(127, int(hand.palm_position[1] * 0.18))
        hand_id = hand.id % 100

        # avoid noise
        if self.note_lock[handType] > 0:
            self.note_lock[handType] -= 1

        if self.pre_y_speed[hand_id] > -200\
                and y_speed <= -200:

            note_generator.set_chord(lib.MusicPlayer.CHORD)
            #note = note_generator.create_tone_note(x_pos)
            note = note_generator.create_note_mix(x_pos, 0.5)
            self.send_note_midi(note, handType, velo)

        self.pre_y_speed[hand_id] = y_speed

        if abs(y_speed) < 200:
            for finger in hand.fingers:
                self.finger_func(finger, handType)

        return handType

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        isDead = [True, True]
        for hand in frame.hands:
            handType = self.hand_func(hand)
            isDead[handType] = False

        for i, state in enumerate(isDead):
            if state:
                if self.pre_note[i]:
                    midiout.send_message(
                        note_off(i, self.pre_note[i]))
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

    t1 = threading.Thread(target=play_music)
    t1.start()
    # Keep this process running until Enter is pressed
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
        controller.remove_listener(listener)


def test_midi():
    while not Flags.FINISH:
        note_generator.set_chord(lib.MusicPlayer.CHORD)
        n = note_generator.create_tone_note(random.random())
        print(note_generator.tone_note_list())
        print(lib.MusicPlayer.CHORD)
        print(n)
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
