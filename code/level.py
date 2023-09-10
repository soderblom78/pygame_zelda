import os

import pygame
from settings import *
from tile import Tile
from player import Player
from debug import Debug
from ui import UI
from weapon import Weapon
from enemy import Enemy
from particles import ParticleEffect
from collect_items import CollectItems
import os


class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        # sprite group setup
        self.visible_sprites = YsortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.rock = "rock"
        self.bush = "bush"
        self.tree = "tree"
        self.treasure_under_bush = "treasure_under_bush"

        # import sprite animation frames
        self.bush_animation_frames = []
        self.item_animation_frames = []
        file_directory_path = "../graphics/bush/"
        for img in range(len(os.listdir(file_directory_path))):
            image = pygame.image.load(f"{file_directory_path}{img}.png").convert_alpha()
            self.bush_animation_frames.append(image)

        file_directory_path = "../graphics/items/"
        for img in range(len(os.listdir(file_directory_path))):
            image = pygame.image.load(f"{file_directory_path}{img}.png").convert_alpha()
            self.item_animation_frames.append(image)

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

    def create_map(self):
        list_enemy_location = []
        for row_index, row in enumerate(world_map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == self.rock:
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites], self.rock)
                if col == self.bush:
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], self.bush)
                if col == self.treasure_under_bush:
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], self.treasure_under_bush)
                if col == self.tree:
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites], self.tree, )
                if col == "enemy":
                    list_enemy_location.append([x, y])

        for row in list_enemy_location:
            Enemy("beast",
                  (row[0], row[1]),
                  [self.visible_sprites, self.attackable_sprites],
                  self.obstacle_sprites,
                  self.damage_player)

        self.player = Player(
            (3200, 3200),
            [self.visible_sprites],
            self.obstacle_sprites,
            self.create_attack,
            self.destroy_attack,
            self.create_magic)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        print(style)
        print(strength)
        print(cost)

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprite = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprite:
                    for target_sprite in collision_sprite:
                        if target_sprite.sprite_type == self.bush or target_sprite.sprite_type == self.treasure_under_bush:
                            particles = ParticleEffect(target_sprite.rect.center, self.bush_animation_frames, [self.visible_sprites])
                            target_sprite.kill()
                            if target_sprite.sprite_type == self.treasure_under_bush:
                                collect_items = CollectItems(target_sprite.rect.center, self.item_animation_frames, [self.visible_sprites])
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            # spawn particles

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)
        Debug(self.display_surface.get_width())


class YsortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        # creating the floor
        self.floor_surf = pygame.image.load("../graphics/tile_map/roger_map3.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)
        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)


    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites()if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)










