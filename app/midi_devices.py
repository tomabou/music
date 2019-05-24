
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
