import pygame
from src.settings import BAR_COLOR, BAR_COLOR_SELECTED, UI_FONT, UI_FONT_SIZE
from src.support import import_csv_chat_tree, TextNode
import random



class ChatBox:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.color = BAR_COLOR_SELECTED

        self.make_rect()

        self.counter = 0
        self.text_speed = 3
        self.done = True

        self.chattrees = import_csv_chat_tree('./chat_trees')
        self.chat_type = 'Bully'
        self.curNode = random.choice(self.chattrees[self.chat_type])
        self.cur_choice = 0

        self.status = 'ongoing'

        self.set_message()

    def make_rect(self):
        left = self.display_surface.get_size()[0] * 0.05
        top = self.display_surface.get_size()[1] * 0.7
        width = self.display_surface.get_size()[0] * 0.9
        height = self.display_surface.get_size()[1] * 0.25
        self.rect = pygame.Rect(left, top, width, height)

    def draw_box(self):
        pygame.draw.rect(self.display_surface, self.color, self.rect)

    def set_message(self):
        self.message = ""
        self.counter = 0
        self.done = False

        if self.curNode is None:
            return

        self.message = self.curNode.text 

    def inputs(self):
        if not self.done:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            nxt_node = self.curNode.get_next_node(self.cur_choice)
            if nxt_node is None:
                self.status = self.curNode.action_type
            else:
                self.curNode = nxt_node
            self.set_message()

    def display(self):
        self.inputs()
        self.draw_box()

        if self.counter < self.text_speed * len(self.message):
            self.counter += 1
        else:
            self.done = True

        snip = self.font.render(self.message[0:self.counter//self.text_speed], True, 'white')
        x = self.rect.left + 10
        y = self.rect.top + 10
        self.display_surface.blit(snip, (x, y))
