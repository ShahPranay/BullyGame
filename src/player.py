import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -26)

        self.direction = pygame.math.Vector2()
        self.speed = 5

        # movement 
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        # attack input 
        if keys[pygame.K_SPACE]:
            self.attacking = True
            # self.attack_time = pygame.time.get_ticks()
            # self.create_attack()
            # self.weapon_attack_sound.play()

        # magic input 
        if keys[pygame.K_LCTRL]:
            self.attacking = True
            # self.attack_time = pygame.time.get_ticks()
            # style = list(magic_data.keys())[self.magic_index]
            # strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
            # cost = list(magic_data.values())[self.magic_index]['cost']
            # self.create_magic(style,strength,cost)

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        # if self.attacking:
        #      if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
        #         self.attacking = False
        #         self.destroy_attack()

        # if not self.can_switch_weapon:
        #      if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
        #           self.can_switch_weapon = True
                  
        # if not self.can_switch_magic:
        #      if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
        #           self.can_switch_magic = True
                  
        # if not self.vulnerable:
        #     if current_time - self.hurt_time >= self.invulnerability_duration:
        #         self.vulnerable = True

    def update(self):
        self.input()
        self.move(self.speed)
