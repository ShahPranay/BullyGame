import pygame
from src.settings import *
from src.tile import Tile
from src.player import Player
from src.debug import debug

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        for row_ind, row in enumerate(WORLD_MAP):
            for col_ind, col in enumerate(row):
                x = col_ind * TILESIZE
                y = row_ind * TILESIZE
                
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                elif col == 'p':
                    self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player: Player):
        # getting the offset
        self.offset.x = -player.rect.centerx + self.half_width
        self.offset.y = -player.rect.centery + self.half_height

        for sprite in self.sprites():
            offset_pos = sprite.rect.center + self.offset
            self.display_surface.blit(sprite.image, offset_pos)
