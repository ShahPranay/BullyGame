import pygame
from src.settings import *

class Menu:
    def __init__(self,player):
        #general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

    def input(self):
        keys = pygame.key.get_pressed()

        



    def display_menu(self):
        self.display_surface.fill('black')