import pygame.midi
import pygame
import time
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


for i in range(10):
    for i in [64, 66, 68, 69, 71, 69, 68, 66, ]:
        playnote(i-4)


del player
pygame.midi.quit()
