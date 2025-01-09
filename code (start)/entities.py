from settings import *


# Parent für Player und alle anderen Characters
class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(groups)

        # graphics
        self.frame_index, self.frames = 0, frames
        
        # self.direction = vector()
        # self.speed = 250
        # self.blocked = False
        
        # sprite setup
        self.image = self.frames['down'][self.frame_index]
        self.rect = self.image.get_frect(center=pos)
        # self.hitbox = self.rect.inflate(-self.rect.width / 2, -60)

        # self.y_sort = self.rect.centery


# unser basic Player
class Player(Entity):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)

        self.direction = vector()

    # bewegung eingabe
    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector()

        if keys[pygame.K_UP]:
            input_vector.y -= 1
        if keys[pygame.K_DOWN]:
            input_vector.y += 1
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        self.direction = input_vector

    # bewegungsmethode und movement speed
    def move(self, dt):
        self.rect.center += self.direction * 250 * dt

    # neue pos updaten
    def update(self, dt):
        self.input()
        self.move(dt)
