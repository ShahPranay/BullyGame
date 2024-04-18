import pygame
from src.settings import *
from src.support import import_csv_chat_tree, TextNode
import random

class ChatBox:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.make_rects()

        self.counter = 0
        self.text_speed = 3
        self.done = True

        self.curNode = None
        self.cur_choice = 0

        self.status = 'ongoing'

        self.set_message()

        self.can_change_choice = True
        self.choice_change_time = 0

    def set_chat_node(self, talking_to):
        self.curNode = talking_to.chat_node
        self.set_message()

    def make_rects(self):
        left = self.display_surface.get_size()[0] * 0.05
        top = self.display_surface.get_size()[1] * 0.7
        chatbox_width = self.display_surface.get_size()[0] * 0.9
        chatbox_height = self.display_surface.get_size()[1] * 0.25
        self.rect = pygame.Rect(left, top, chatbox_width, chatbox_height)

        choice_width = 150
        choice_height = 50
        gap = 150
        top = self.rect.bottom - 80
        left = left + (chatbox_width - (2 * choice_width + gap)) // 2 
        self.pos_choice_rect = pygame.Rect(left, top, choice_width, choice_height)
        self.neg_choice_rect = pygame.Rect(left + choice_width + gap, top, choice_width, choice_height)

    def draw_box(self):
        pygame.draw.rect(self.display_surface, CHATBOX_COLOR, self.rect)

    def draw_choices(self):
        getcolor = lambda cid : CHOICE_COLOR_SELECTED if cid == self.cur_choice else CHOICE_COLOR

        x = self.pos_choice_rect.left + 15
        y = self.pos_choice_rect.top + 15
        pygame.draw.rect(self.display_surface, getcolor(0), self.pos_choice_rect)
        snip = self.font.render("Positive", True, getcolor(1))
        self.display_surface.blit(snip, (x,y))

        x = self.neg_choice_rect.left + 15
        y = self.neg_choice_rect.top + 15
        pygame.draw.rect(self.display_surface, getcolor(1), self.neg_choice_rect)
        snip = self.font.render("Negative", True, getcolor(0))
        self.display_surface.blit(snip, (x,y))

    def set_message(self):
        self.message = ""
        self.counter = 0
        self.cur_choice = 0
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
            self.curNode = nxt_node
            if self.curNode is  None:
                print("status changed to finished")
                self.status = 'finished'
                return
            self.set_message()
        
        if not self.can_change_choice:
            return

        if keys[pygame.K_LEFT]:
            self.cur_choice -= 1
            self.cur_choice = (self.cur_choice + 2) % 2
            self.can_change_choice = False
            self.choice_change_time = pygame.time.get_ticks()
        elif keys[pygame.K_RIGHT]:
            self.cur_choice += 1
            self.cur_choice %= 2
            self.can_change_choice = False
            self.choice_change_time = pygame.time.get_ticks()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if not self.can_change_choice:
            if current_time - self.choice_change_time >= 150:
                self.can_change_choice = True

    def display(self):
        self.cooldowns()
        self.inputs()
        if self.curNode is None:
            return
        self.draw_box()

        if self.counter < self.text_speed * len(self.message):
            self.counter += 1
        else:
            self.done = True

        snip = self.font.render(self.message[0:self.counter//self.text_speed], True, 'white')
        x = self.rect.left + 30
        y = self.rect.top + 30
        self.display_surface.blit(snip, (x, y))

        if self.done and self.curNode.get_choice_cnt() == 2:
            self.draw_choices()
