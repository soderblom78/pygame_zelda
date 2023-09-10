import random

# game setup
WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64

# world setup
cell = ["rock", " ", "bush", "tree", "treasure_under_bush"]
cell2 = [" ", "tree"]
world_map = []

for i in range(100):
    row = [cell[1] for i in range(100)]
    world_map.append(row)

for x in range(100):
    for y in range(100):
        select_random = random.randint(1, 10)
        random_object = random.choice(cell)
        select_random_enemy = random.randint(1, 200)
        random_enemy = "enemy"
        if select_random == 1:
            world_map[x][y] = random_object
        if select_random_enemy == 1:
            world_map[x][y] = random_enemy
        if x == 20:
            world_map[x][y] = cell[0]
        if y == 20:
            world_map[x][y] = cell[0]
        if x in range(48, 55) and y in range(48, 55):
            world_map[x][y] = cell[1]
        if x == 80:
            world_map[x][y] = cell[0]

# weapons
weapon_data = {
    "sword": {"cooldown": 100, "damage": 15, "graphic": "../graphics/weapon/sword/full.png"},
    "lance": {"cooldown": 400, "damage": 30, "graphic": "../graphics/weapon/lance/full.png"},
    "axe": {"cooldown": 300, "damage": 20, "graphic": "../graphics/weapon/axe/full.png"},
    "rapier": {"cooldown": 50, "damage": 8, "graphic": "../graphics/weapon/rapier/full.png"},
    "sai": {"cooldown": 80, "damage": 10, "graphic": "../graphics/weapon/sai/full.png"}}

magic_data = {
    "flame": {"strength": 5, "cost": 20, "graphic": "../graphics/particles/flame/flame.png"},
    "heal": {"strength": 20, "cost": 10, "graphic": "../graphics/particles/heal/heal.png"}}

monster_data = {"beast": {"health": 100,
                          "exp": 100,
                          "damage": 20,
                          "attack_type": "slash",
                          "attack_sound": "../sound/attack/jump.waw",
                          "speed": 3,
                          "resistance": 3,
                          "attack_radius": 80,
                          "notice_radius": 360}}


# ui setup
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = "../graphics/fonts/joystix monospace.ttf"
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = "#71ddee"
UI_BG_COLOR = "#222222"
UI_BORDER_COLOR = "#111111"
TEXT_COLOR = "#EEEEEE"

# ui colors
HEALTH_COLOR = "red"
ENERGY_COLOR = "blue"
UI_BORDER_COLOR_ACTIVE = "gold"








