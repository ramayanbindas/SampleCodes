'''
:about: This project is the demo of seven-segment-display made by the module pygame.
This code doesn't related to any of the code need to create seven-segment display.
This code only show case how it may be the code-version of seven-segment display.

What is seven-segment display?
-> Seven-segment display is display device which takes 7 inputs and produce output base on
the inputs. It is type of display which generally divide into seven segment to represent some
things like number, alphabet etc.
It is mostly used in displaying a time in railway station, digital clock.

:author: Ramayan Mardi
'''

import pygame
from pygame.locals import *
from sys import exit

import time


class SegmentClock:
    ''':class: Used to create a clock with the help of seven-segment display'''

    def __init__(self, pos: tuple[int], **config):
        self.segment_objects = []
        for i in range(6):
            spacing = 10
            if (i + 1) % 2 == 0:
                spacing = 30
            self.segment_objects.append(SevenSegmentDisplay(pos=pos, **config))
            pos = (self.segment_objects[-1].rect.topright[0] + spacing, pos[1])

    def update(self, surf: pygame.surface):
        current_time = list(time.strftime("%I%M%S"))
        for index, segment in enumerate(self.segment_objects):
            segment.update(surf, int(current_time[index]))
            if (index + 1) % 2 == 0:
                spacing = 15
                point1 = (segment.rect.topright[0] + spacing, segment.rect.y + 10, 10, 10)
                pygame.draw.rect(surf, "red", point1)
                point2 = (segment.rect.topright[0] + spacing, segment.rect.bottom - 10, 10, 10)
                pygame.draw.rect(surf, "red", point2)


class SevenSegmentDisplay:
    ''':class: create or display a number [0-9] in the form of seven segment display'''

    def __init__(self, pos: tuple[int] = (0, 0), **config):
        size = config.pop("size", config.pop("s", (80, 100)))
        segment_width = config.pop("segment_width", config.pop("seg_w", 4))
        background_color = config.pop("background", config.pop("bg", None))
        on_color = config.pop("on_color", "red")
        off_color = config.pop("off_color", "white")

        self.rect = pygame.Rect(pos, size)

        # color of the segment when the segment is off
        self.OFF_COLOR = off_color
        # color of the segment when the color is on
        self.ON_COLOR = on_color
        # background color of the segment (mainly the bounding box)
        self.BACKGROUND_COLOR = background_color
        # width of the each segment
        self.SEGMENT_WIDTH = segment_width

        self.display_data = {1: {"start_pos": self.rect.topleft, "end_pos": self.rect.topright},
                             2: {"start_pos": self.rect.topright,
                                 "end_pos": (self.rect.topright[0], self.rect.centery)},
                             3: {"start_pos": (self.rect.topright[0], self.rect.centery),
                                 "end_pos": self.rect.bottomright},
                             4: {"start_pos": self.rect.bottomright,
                                 "end_pos": self.rect.bottomleft},
                             5: {"start_pos": self.rect.bottomleft,
                                 "end_pos": (self.rect.topleft[0], self.rect.centery)},
                             6: {"start_pos": (self.rect.topleft[0], self.rect.centery),
                                 "end_pos": self.rect.topleft},
                             7: {"start_pos": (self.rect.topleft[0] + self.SEGMENT_WIDTH,
                                               self.rect.centery),
                                 "end_pos": (self.rect.topright[0] - self.SEGMENT_WIDTH,
                                             self.rect.centery)}}

        self.signal_data = {0: [1, 1, 1, 1, 1, 1, 0],
                            1: [0, 1, 1, 0, 0, 0, 0],
                            2: [1, 1, 0, 1, 1, 0, 1],
                            3: [1, 1, 1, 1, 0, 0, 1],
                            4: [0, 1, 1, 0, 0, 1, 1],
                            5: [1, 0, 1, 1, 0, 1, 1],
                            6: [1, 0, 1, 1, 1, 1, 1],
                            7: [1, 1, 1, 0, 0, 1, 0],
                            8: [1, 1, 1, 1, 1, 1, 1],
                            9: [1, 1, 1, 1, 0, 1, 1]}

    def structure(self, surf: pygame.surface, num: int = 0):
        ''':method: create the structure of the seven-segment display'''

        count = 0
        for key, items in self.display_data.items():
            color = self.OFF_COLOR
            start_pos = items["start_pos"]
            end_pos = items["end_pos"]
            if self.signal_data[num][count]:
                color = self.ON_COLOR
            pygame.draw.line(surf, color, start_pos, end_pos, self.SEGMENT_WIDTH)
            count += 1

    def update(self, surf: pygame.display, num: int):
        '''
            :method: used to display the segment to the screen
            :param num: number should be displayed on the screen range [0-9]
        '''
        if self.BACKGROUND_COLOR:
            pygame.draw.rect(surf, self.BACKGROUND_COLOR, self.rect)
        self.structure(surf, int(num) if num < 10 else 0)


class Game:
    def __init__(self, window_size: tuple[int] = (640, 480), *config):
        self.display = pygame.display.set_mode(window_size, *config)
        pygame.display.set_caption("Seven-Segment Display Demo")

        self.clock = pygame.time.Clock()
        self.FPS = 30

    def run(self):
        ''':method: controls whole game.'''

        pos = (200, 185)
        segment_clock = SegmentClock(pos=pos, size=(30, 50), off_color="#733434")

        running = True
        while running:
            self.display.fill("#362626")

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    running = False

            segment_clock.update(self.display)
            pygame.display.update()
            self.clock.tick(self.FPS)

        pygame.quit()
        exit()


if __name__ == '__main__':
    Game().run()
