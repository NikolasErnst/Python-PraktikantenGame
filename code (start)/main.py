from settings import *
from pytmx.util_pygame import load_pygame
from os.path import join
from sprites import Sprite
from entities import Player
from groups import AllSprites
from monster import Monster
from monsterIndex import MonsterIndex
class Game:
    # generell
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Atruvimon")
        self.clock = pygame.time.Clock()

        # groups
        self.all_sprites = AllSprites()

        self.import_assets()
        self.setup(self.tmx_maps['world'],'house')
        
        # player monsters 
        self.player_monsters = {
			0: Monster('Plumette', 31),
		}      
        
        #fonts
        self.fonts = {
			'dialog': pygame.font.Font(join('..', 'graphics', 'fonts', 'PixeloidSans.ttf'), 30),
			'regular': pygame.font.Font(join('..', 'graphics', 'fonts', 'PixeloidSans.ttf'), 18),
			'small': pygame.font.Font(join('..', 'graphics', 'fonts', 'PixeloidSans.ttf'), 14),
			'bold': pygame.font.Font(join('..', 'graphics', 'fonts', 'dogicapixelbold.otf'), 20),
		}
        
        # overlays 
        self.dialog_tree = None
        self.monster_index = MonsterIndex(self.player_monsters, self.fonts)
        self.index_open = False
        self.battle = None
        self.evolution = None
        
        
        #trash for testing
        color = (255, 0, 0)
        self.display_surface.fill(color)

    def import_assets(self):
        self.tmx_maps = {"world": load_pygame(join("..", "data", "maps", "world.tmx"))}

    def setup(self, tmx_map, player_start_pos):
        for x, y, surf in tmx_map.get_layer_by_name("Terrain").tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        for obj in tmx_map.get_layer_by_name("Entities"):
            if obj.name == "Player" and obj.properties["pos"] == player_start_pos:
                self.player = Player((obj.x, obj.y), self.all_sprites)
                
    def input(self):
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_SPACE]:
            self.index_open = not self.index_open
            
        
    # loop 
    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # logik
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
            self.input() 
            
            #overlays
            if self.index_open: self.monster_index.update(dt)
            

if __name__ == "__main__":
    game = Game()
    game.run()
