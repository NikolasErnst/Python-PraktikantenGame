from settings import *
from pytmx.util_pygame import load_pygame
from os.path import join
from sprites import Sprite, AnimatedSprite
from entities import Player, Character
from groups import AllSprites
from support import *
from dialog import DialogTree
from game_data import *


class Game:
    # generell
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Atruvimon")
        self.clock = pygame.time.Clock()

        # groups
        self.all_sprites = AllSprites()
        self.dialog_tree = None
        # Importiere Assets
        self.import_assets()

        # Verwalte alle notwendigen Attribute
        self.player = None
        self.setup_done = False  # Flag, um zu prüfen, ob Setup durchgeführt wurde

    def import_assets(self):
        self.tmx_maps = {
            "world": load_pygame(join("..", "data", "maps", "world.tmx")),
            "hospital": load_pygame(join("..", "data", "maps", "hospital.tmx")),
        }
        self.overworld_frames = {
            "water": import_folder("..", "graphics", "tilesets", "water"),
            "coast": coast_importer(24, 12, "..", "graphics", "tilesets", "coast"),
            "characters": all_character_import("..", "graphics", "characters"),
        }
            #Schriftart
        self.fonts = {
            'dialog': pygame.font.Font(join('..', 'graphics', 'fonts', 'PixeloidSans.ttf'), 30)
        }

    def setup(self, tmx_map, player_start_pos):
        # Terrain und Terrain Top Setup
        for layer in ["Terrain", "Terrain Top"]:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        # Objects
        for obj in tmx_map.get_layer_by_name("Objects"):
            Sprite((obj.x, obj.y), obj.image, self.all_sprites)

        # Entities
        for obj in tmx_map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                if obj.properties["pos"] == player_start_pos:
                    self.player = Player(
                        pos=(obj.x, obj.y),
                        frames=self.overworld_frames["characters"]["player"],
                        groups=self.all_sprites,
                    )
            else:
                Character(
                    pos=(obj.x, obj.y),
                    frames=self.overworld_frames["characters"]["player"],
                    groups=self.all_sprites,
                )

        # Water
        for obj in tmx_map.get_layer_by_name("Water"):
            for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
                for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
                    AnimatedSprite(
                        (x, y), self.overworld_frames["water"], self.all_sprites
                    )

        # Coast
        for obj in tmx_map.get_layer_by_name("Coast"):
            terrain = obj.properties["terrain"]
            side = obj.properties["side"]
            AnimatedSprite(
                (obj.x, obj.y),
                self.overworld_frames["coast"][terrain][side],
                self.all_sprites,
            )

    def input(self):
        if not self.dialog_tree:
            keys = pygame.key_get_just_pressed()
        if keys[pygame.K_SPACE]:
            for character in self.character_sprites:
                if check_connections(100, self.player, character):
                    self.player.block()#block movement while dialog
                    self.create_dialog()#create dialog
                    print('dialog')

    def create_dialog(self, character):
        if not self.dialog_tree:
            self.dialog_tree = DialogTree(character, self.player, self.all_sprites, self.fonts['dialog'], self.end_dialog)

    def end_dialog(self, character):
        self.dialog_tree = None
        self.player.unblock()
    # run loop
    def run(self):
        # Setup wird nun hier aufgerufen, nachdem alle Variablen initialisiert wurden
        if not self.setup_done:
            self.setup(self.tmx_maps["world"], "house")
            self.setup_done = True

        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # game logic
            self.all_sprites.update(dt)
            self.display_surface.fill("black")
            self.all_sprites.draw(self.player.rect.center)  # Bezieht sich auf den Player

            if self.dialog_tree: self.dialog_tree.update()
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
