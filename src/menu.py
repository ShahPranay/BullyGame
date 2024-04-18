import pygame
from src.settings import *

class Menu:
    def __init__(self,player):
        #general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # item dimensions
        self.heigth = self.display_surface.get_size()[1]*0.3
        self.width = self.display_surface.get_size()[0]*0.3

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
        self.option_list = ['Restart', 'Quit']

        for option in range(2):
            full_width = self.display_surface.get_size()[0]
            increment = full_width // 2
            left = (option * increment) + (increment - )

    def display_menu(self):
        self.display_surface.fill('black')
        self.input()
        self.selection_cooldown()