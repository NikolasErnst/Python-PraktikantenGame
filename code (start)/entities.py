from settings import *


# Parent für Player und alle anderen Characters
class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(groups)
        self.z = WORLD_LAYERS["main"]
        #char grafik für richtige richtung animation 
        self.frame_index, self.frames = 0, frames
        self.facing_direction = 'down'
        #movement
        self.direction = vector()
        self.speed = 250
        self.blocked = False
        #sprite setup
        self.image = self.frames[self.get_state()][self.frame_index]
        self.rect = self.image.get_frect(center=pos)

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[self.get_state()][
            int(self.frame_index % len(self.frames[self.get_state()]))
        ]
    #abfrage ob gelaufen wird oder idle 
    def get_state(self):
        moving = bool(self.direction)
        if moving:
            if self.direction.x != 0:
                self.facing_direction = "right" if self.direction.x > 0 else "left"
            if self.direction.y != 0:
                self.facing_direction = "down" if self.direction.y > 0 else "up"
        return f"{self.facing_direction}{'' if moving else '_idle'}"

    def block(self):
        self.blocked = True
        self.direction = vector(0,0)
        
    def unblock(self):
        self.blocked = False

# unser basic Player
class Player(Entity):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.direction = vector()

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

    def move(self, dt):
        self.rect.center += self.direction * 250 * dt

    def update(self, dt):
        self.input()  # Nur der Player sollte Eingabe haben
        self.move(dt)
        self.animate(dt)  


class Character(Entity):       
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        # print(character_data)
        self.direction = vector()
    def get_dialog(self):
        return 'Ich bin Vertriebler.', 'Ich habe dual Wirtschaftsinformatik Sales & Consulting studiert.', 'Jetzt bin ich in Neukundenaquise und Kundenbetreeung tätig.'
    # Keine Eingabemethoden für Character
    def move(self, dt):
        self.rect.center += self.direction * 250 * dt

    def update(self, dt):
        self.animate(dt)
        if not self.blocked:
            self.move(dt)
