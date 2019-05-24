
import lib.Leap as Leap
import sys
import thread
import time

import pygame.midi
import pygame

pygame.init()
pygame.midi.init()
count = pygame.midi.get_count()
print("get_default_input_id:%d" % pygame.midi.get_default_input_id())
print("get_default_output_id:%d" % pygame.midi.get_default_output_id())
print("No:(interf, name, input, output, opened)")
for i in range(count):
    print("%d:%s" % (i, pygame.midi.get_device_info(i)))
player = pygame.midi.Output(6)
player.set_instrument(0)


def playnote(note):
    player.note_on(note, 127)
    time.sleep(0.5)
    player.note_off(note, 127)


class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    pre_y_speed = [1, 2]
    pre_note = [60, 60]

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))

        isDead = [True, True]
        # Get hands
        for hand in frame.hands:

            handType = 0 if hand.is_left else 1
            isDead[handType] = False

            y_speed = hand.palm_velocity[1]
            x_pos = hand.palm_position[0]
            print " %d " % (x_pos)

            note = 60 + nearest_note(int(x_pos) // 20)

            if self.pre_y_speed[handType] > -50 and y_speed <= -50:
                player.note_on(note, 127)
                if self.pre_note[handType] != None and note != self.pre_note[handType]:
                    player.note_off(self.pre_note[handType], 127)
                self.pre_note[handType] = note
                print "note on"
            if self.pre_y_speed[handType] < 0 and y_speed > 0:
                print "note off"

            self.pre_y_speed[handType] = y_speed

            print "  %s, id %d, velocity: %s" % (
                handType, hand.id, hand.palm_velocity)

        print isDead
        for i, state in enumerate(isDead):
            if state:
                if self.pre_note[i]:
                    player.note_off(self.pre_note[i], 127)
                self.pre_note[i] = None

        if not frame.hands.is_empty:
            print ""


def nearest_note(x):
    for i in range(3):
        if (x+i) % 12 in [0, 2, 4,  7, 9]:
            return (x + i)


def main():
    # Create a sample listener and controller
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
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
    del player
    pygame.midi.quit()
