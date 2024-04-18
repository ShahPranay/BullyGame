import pygame
from src.settings import *

class Menu:
    def __init__(self,player):
        #general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.isRestart = False
        self.isQuit = False

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
                if self.selection_index == 0:
                    self.isRestart = True      
                if self.selection_index == 1:
                    self.isQuit = True
        
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
        self.option_list[0].display(self.display_surface,self.selection_index, 'Restart')
        self.option_list[1].display(self.display_surface,self.selection_index, 'Quit')
        

class Item:
    def __init__(self,l,t,w,h,index,font):
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index
        self.font = font

    def display_names(self, surface, name, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(center = self.rect.center + pygame.math.Vector2(0,0))

        surface.blit(title_surf, title_rect)

    def display(self, surface, selection_num, name):
        if selection_num == self.index:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR,self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR,self.rect, 4)

        self.display_names(surface, name, self.index == selection_num)