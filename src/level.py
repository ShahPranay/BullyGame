import pygame, sys
from src.bully import Enemy
from src.settings import *
from src.tile import Tile
from src.player import Player
from src.debug import debug
from src.support import *
from random import choice, randint
from src.weapon import Weapon
from src.ui import UI
# from src.bully import Bully
from src.particles import AnimationPlayer
from src.magic import MagicPlayer
from src.chatbox import ChatBox
from src.story import Story
from src.menu import Menu

class Level:
    def __init__(self):

        # get the display surface 
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # chatbox
        self.is_talking = False
        self.chatbox = ChatBox()
        self.entity_map = {}

        # sprite setup
        self.create_map()
        self.story = Story(self)

        # user interface 
        self.ui = UI()
        self.menu = Menu(self.player)

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        self.gameover = False
        self.gameover_narrator = False


    def create_map(self):
        layouts = {
                'boundary': import_csv_layout('./map/map_FloorBlocks.csv'),
                'grass': import_csv_layout('./map/map_Grass.csv'),
                'entities': import_csv_layout('./map/map_Entities.csv')
                }
        graphics = {
                'grass': import_folder('./graphics/grass'),
                }

        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites],'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile(
                                    (x,y),
                                    [self.visible_sprites,self.obstacle_sprites,self.attackable_sprites],
                                    'grass',
                                    random_grass_image)

                        if style == 'object' and self.story.isPantyAvailable:
                            surf = graphics['objects'][0]
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites,self.attackable_sprites],'object',surf)

                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                        (x,y),
                                        [self.visible_sprites],
                                        self.obstacle_sprites,
                                        self.create_attack,
                                        self.destroy_attack,
                                        self.create_magic)
                                self.entity_map['player'] = self.player
                            # else:
                            #     if col == '390': monster_name = 'bamboo'
                            #     elif col == '391': monster_name = 'spirit'
                            #     elif col == '392': monster_name ='raccoon'
                            #     else: monster_name = 'squid'
        self.entity_map['bully1'] = Enemy(
                'bully1',
                (5000,2200),
                [self.visible_sprites],
                self.obstacle_sprites,
                self.initiate_chat,
                self.damage_player,
                self.trigger_death_particles,
                self.add_exp)

        self.entity_map['narrator'] = Enemy(
                'bully1',
                self.player.rect.center,
                [],
                self.obstacle_sprites,
                self.initiate_chat,
                self.damage_player,
                self.trigger_death_particles,
                self.add_exp)

        self.entity_map['narrator'].speed = 7

    def create_panty(self):
        layout = import_csv_layout('./map/map_Objects.csv')
        graphics = {'objects': import_folder('./graphics/objects')}
        for row_index,row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col != '-1':
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE
                    surf = graphics['objects'][0]
                    Tile((x,y),[self.visible_sprites,self.obstacle_sprites,self.attackable_sprites],'object',surf)

    def create_bully2(self):
        self.entity_map['bully2'] = Enemy(
                'bully2',
                (3635,1338),
                [self.visible_sprites],
                self.obstacle_sprites,
                self.initiate_chat,
                self.damage_player,
                self.trigger_death_particles,
                self.add_exp)
        
    
    def create_bully3(self):
        self.entity_map['bully3'] = Enemy(
                'bully3',
                (1719,1079),
                [self.visible_sprites],
                self.obstacle_sprites,
                self.initiate_chat,
                self.damage_player,
                self.trigger_death_particles,
                self.add_exp)

    def create_bully4(self):
        self.entity_map['bully4'] = Enemy(
                'bully4',
                (3259,2645),
                [self.visible_sprites],
                self.obstacle_sprites,
                self.initiate_chat,
                self.damage_player,
                self.trigger_death_particles,
                self.add_exp)

    def create_security(self):
        self.entity_map['security'] = Enemy(
                'security',
                (716,2799),
                [self.visible_sprites],
                self.obstacle_sprites,
                self.initiate_chat,
                self.damage_player,
                self.trigger_death_particles,
                self.add_exp)

    def make_entity_attakable(self, entity):
        self.attackable_sprites.add(entity)

    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])

    def create_magic(self,style,strength,cost):
            self.magic_player.rock(self.player,[self.visible_sprites,self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            self.player.grass_cnt += 1
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,75)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos - offset,[self.visible_sprites])
                            target_sprite.kill()
                        elif target_sprite.sprite_type == 'object':
                            self.player.panty_cnt += 1
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player,attack_sprite.sprite_type)

    def initiate_chat(self, talking_to):
        self.chatbox.set_chat_node(talking_to)
        self.is_talking = True
        self.chatbox.status = 'ongoing'
        self.talking_to = talking_to

    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])

    def trigger_death_particles(self,pos,particle_type):

        self.animation_player.create_particles(particle_type,pos,self.visible_sprites)

    def add_exp(self,amount):

        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused 

    def run(self):
        self.entity_map['narrator'].origin = self.player.rect.center
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        self.story.update()

        if self.gameover:
            self.game_paused = True

        if self.is_talking:
            # print("is talking is true, " , self.chatbox.status)
            if self.chatbox.status == 'ongoing':
                self.chatbox.display()
            else:
                self.is_talking = False
                self.talking_to.finished_chat = True
                self.talking_to.chat_node = None
        elif self.game_paused:
            self.menu.display_menu()
            if self.menu.isRestart:
                self.menu.isRestart = False
                self.__init__()
            if self.menu.isQuit:
                pygame.quit()
                sys.exit()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.entity_map['narrator'].update()
            self.entity_map['narrator'].enemy_update(self.player)
            self.player_attack_logic()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup 
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load('./graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self,player):

        # getting the offset 
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
