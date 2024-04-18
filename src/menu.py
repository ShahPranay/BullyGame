import pygame
from src.settings import *

class Menu:
    def __init__(self,player):
        #general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # item creation
        self.heigth = self.display_surface.get_size()[1]*0.3
        self.width = self.display_surface.get_size()[0]*0.3
        self.create_options()

        # selection system
        self.selection_index = 0
        self.selection_time = None
        self.can_select = True

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_select:
            if keys[pygame.K_RIGHT]:
                self.selection_index = 1
                self.can_select = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT]:
                self.selection_index = 0
                self.can_select = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_select = False
                self.selection_time = pygame.time.get_ticks()
                print(self.selection_index)
        
    def selection_cooldown(self):
        if not self.can_select:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_select = True

    def create_options(self):
        self.option_list = []

        # for option, index in range(2):
        full_width = self.display_surface.get_size()[0]
        increment = full_width // 2
        left1 = (0 * increment) + (increment - self.width) // 2
        left2 = (1 * increment) + (increment - self.width) // 2
        top = self.display_surface.get_size()[1] * 0.4
        item1 = Item(left1,top,self.width,self.heigth,0,self.font)
        self.option_list.append(item1)
        item2 = Item(left2,top,self.width,self.heigth,1,self.font)
        self.option_list.append(item2)
            

    def display_menu(self):
        self.input()
        self.selection_cooldown()

        for item in self.option_list:
            item.display(self.display_surface,0, 'test')

class Item:
    def __init__(self,l,t,w,h,index,font):
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index
        self.font = font

    # def display_names(self, surface, name, selected):
        # title_surf = self.font.render(name, False

    def display(self, surface, selection_num, name):
        pygame.draw.rect(surface, UI_BG_COLOR, self.rect)