import pygame
from entity import Entity
from settings import *
import os


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player):

        # general setup
        super().__init__(groups)
        self.image = pygame.image.load("../graphics/test/char_player.png").convert_alpha()
        self.sprite_type = "enemy"

        # graphic setup
        self.status = "idle"
        self.status_direction = "right"
        self.import_graphic(monster_name)

        # movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites
        self.enemy_direction = pygame.math.Vector2()

        # stats
        self.monster_name = monster_name
        monster_name = monster_data[monster_name]
        self.health = monster_name["health"]
        self.exp = monster_name["exp"]
        self.speed = monster_name["speed"]
        self.attack_damage = monster_name["damage"]
        self.resistance = monster_name["resistance"]
        self.attack_radius = monster_name["attack_radius"]
        self.notice_radius = monster_name["notice_radius"]
        self.attack_type = monster_name["attack_type"]

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player

        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

    def import_graphic(self, name):
        list_of_status = []
        character_path = f"../graphics/enemy/{name}"
        for status in os.listdir(character_path):
            list_of_status.append(status)

        self.animations = {
            "idle": {"up": [], "down": [], "left": [], "right": []},
            "move": {"up": [], "down": [], "left": [], "right": []},
            "attack": {"up": [], "down": [], "left": [], "right": []}}

        full_path_list = []
        for status in list_of_status:
            for status_direction in self.animations[status].keys():
                full_path = f"{character_path}/{status}/{status_direction}"
                full_path_list.append(full_path)

        count = 0
        for status in list_of_status:
            for status_direction in self.animations[status].keys():
                for img in os.listdir(full_path_list[count]):
                    img = pygame.image.load(f"{full_path_list[count]}/{img}").convert_alpha()
                    self.animations[status][status_direction].append(img)

                count += 1

    def get_player_distance_and_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return distance, direction

    def get_status(self, player):
        distance = self.get_player_distance_and_direction(player)[0]
        if distance <= self.attack_radius and self.can_attack:
            if self.status != "attack":
                self.frame_index = 0
            self.status = "attack"

        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.status = "idle"

    def get_status_direction(self):
        if self.direction.x < 0:
            self.status_direction = "left"
        elif self.direction.x > 0:
            self.status_direction = "right"
        elif self.direction.y < 0:
            self.status_direction = "up"
        else:
            self.status_direction = "down"

    def actions(self, player):
        if self.status == "attack":
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
        elif self.status == "move":
            self.direction = self.get_player_distance_and_direction(player)[1]

        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status][self.status_direction]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == "attack":
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            # self.direction = self.get_player_distance_and_direction(player)[1]
            if attack_type == "weapon":
                self.health -= player.get_full_weapon_damage()
            else:
                pass
                # magic damage
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance


    def update(self):
        self.hit_reaction()
        self.get_status_direction()
        self.move(self.speed)
        self.animate()
        self.cooldown()
        self.check_death()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)


