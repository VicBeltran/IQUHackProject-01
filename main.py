import pygame, sys
from pygame.locals import *
import random
import time
import pygamepopup
from Quantum_Measure import *

from random import choice

SCREEN_WIDTH = 1000

pygame.init()
FPS = 10
FramePerSec = pygame.time.Clock()

game_font = pygame.font.SysFont('Arial', 20)
 
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

frame = 0
scoreCircuit, playerCircuit, quantumGateDict, quantumRotDict, simulator = initialize(0)
tiles = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

def tiles2coord(row_id: int, col_id: int):
    return(row_id*50, col_id*50)

def tiles2center(row_id: int, col_id: int):
    return(row_id*50 + 25, col_id*50 + 25)

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH + 400,SCREEN_WIDTH))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("Game")
 
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (50,50)) 
        self.rect = self.image.get_rect()
        gen_row = choice(list(range(2,19)))
        indices = [i for i, col in enumerate(tiles[gen_row]) if col == 1]
        gen_col = choice(indices)
        self.rect.center = tiles2center(gen_col, gen_row)
        self.currentdir = (0,0,0,1)
 
    def move(self):
        if not frame:
            legal  = [] # top = 0, down = 1, left = 2, right = 3
            (cur_row, cur_col) = (self.rect.center[1]//50, self.rect.center[0]//50)
            cur_dir = self.currentdir.index(1)
            if tiles[cur_row - 1][cur_col]:
                legal.append(0)
            if tiles[cur_row + 1][cur_col]:
                legal.append(1)
            if tiles[cur_row][cur_col - 1]:
                legal.append(2)
            if tiles[cur_row][cur_col + 1]:
                legal.append(3)
            if cur_dir in legal:
                if cur_dir == 0:
                    self.rect.move_ip(0, -50)
                    return
                elif cur_dir == 1:
                    self.rect.move_ip(0,50)
                    return
                elif cur_dir == 2:
                    self.rect.move_ip(-50, 0)
                    return
                elif cur_dir == 3:
                    self.rect.move_ip(50, 0)
                    return
            move = choice(legal)
            if move == 0:
                self.rect.move_ip(0, -50)
                self.currentdir = (1,0,0,0)
            elif move == 1:
                self.rect.move_ip(0,50)
                self.currentdir = (0,1,0,0)
            elif move == 2:
                self.rect.move_ip(-50, 0)
                self.currentdir = (0,0,1,0)
            else:
                self.rect.move_ip(50, 0)
                self.currentdir = (0,0,0,1)
 
    def draw(self, surface):
        surface.blit(self.image, self.rect) 
 
 
class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (50,50)) 
        self.rect = self.image.get_rect()
        self.rect.center = tiles2center(3, 1)
        self.qGates = []
    
    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        (cur_row, cur_col) = (self.rect.center[1]//50, self.rect.center[0]//50)
        if pressed_keys[K_UP]:
            if tiles[cur_row - 1][cur_col]:
                self.rect.move_ip(0,-50)  
        if pressed_keys[K_DOWN]:
            if tiles[cur_row + 1][cur_col]:
                self.rect.move_ip(0,50)     
        if pressed_keys[K_LEFT]:
            if tiles[cur_row][cur_col - 1]:
                self.rect.move_ip(-50, 0)
        if pressed_keys[K_RIGHT]:
            if tiles[cur_row][cur_col + 1]:
                self.rect.move_ip(50, 0)
 
    def draw(self, surface):
        # (cur_row, cur_col) = (self.rect.center[1]//50, self.rect.center[0]//50)
        surface.blit(self.image, self.rect)     

class HGate(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = "Hadamard"
        self.image = pygame.image.load("Hadamard.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (50,50))
        self.rect = self.image.get_rect()
        gen_row = choice(list(range(2,19)))
        indices = [i for i, col in enumerate(tiles[gen_row]) if col == 1]
        gen_col = choice(indices)
        self.rect.center = tiles2center(gen_col, gen_row)
        tiles[gen_row][gen_col] = 'H'
    
    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

class PZGate(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = "PauliZ"
        self.image = pygame.image.load("Hadamard.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (50,50))
        self.rect = self.image.get_rect()
        gen_row = choice(list(range(2,19)))
        indices = [i for i, col in enumerate(tiles[gen_row]) if col == 1]
        gen_col = choice(indices)
        self.rect.center = tiles2center(gen_col, gen_row)
        tiles[gen_row][gen_col] = 'Z'
    
    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)


class PXGate(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = "PauliX"
        self.image = pygame.image.load("Hadamard.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (50,50))
        self.rect = self.image.get_rect()
        gen_row = choice(list(range(2,19)))
        indices = [i for i, col in enumerate(tiles[gen_row]) if col == 1]
        gen_col = choice(indices)
        self.rect.center = tiles2center(gen_col, gen_row)
        tiles[gen_row][gen_col] = 'X'
    
    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

class PYGate(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = "PauliY"
        self.image = pygame.image.load("Hadamard.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (50,50))
        self.rect = self.image.get_rect()
        gen_row = choice(list(range(2,19)))
        indices = [i for i, col in enumerate(tiles[gen_row]) if col == 1]
        gen_col = choice(indices)
        self.rect.center = tiles2center(gen_col, gen_row)
        tiles[gen_row][gen_col] = 'Y'
    
    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

class RYGate(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = "PauliY"
        self.image = pygame.image.load("Hadamard.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (50,50))
        self.rect = self.image.get_rect()
        gen_row = choice(list(range(2,19)))
        indices = [i for i, col in enumerate(tiles[gen_row]) if col == 1]
        gen_col = choice(indices)
        self.rect.center = tiles2center(gen_col, gen_row)
        tiles[gen_row][gen_col] = 'RY'
    
    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

class RZGate(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = "PauliY"
        self.image = pygame.image.load("Hadamard.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (50,50))
        self.rect = self.image.get_rect()
        gen_row = choice(list(range(2,19)))
        indices = [i for i, col in enumerate(tiles[gen_row]) if col == 1]
        gen_col = choice(indices)
        self.rect.center = tiles2center(gen_col, gen_row)
        tiles[gen_row][gen_col] = 'RZ'
    
    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

class RXGate(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = "PauliY"
        self.image = pygame.image.load("Hadamard.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (50,50))
        self.rect = self.image.get_rect()
        gen_row = choice(list(range(2,19)))
        indices = [i for i, col in enumerate(tiles[gen_row]) if col == 1]
        gen_col = choice(indices)
        self.rect.center = tiles2center(gen_col, gen_row)
        tiles[gen_row][gen_col] = 'RX'
    
    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

class CNOT(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = "PauliY"
        self.image = pygame.image.load("Hadamard.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.center = tiles2center(3,1)
    
    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)
    
         
P1 = Pacman()
E1 = Enemy()
E2 = Enemy()
E3 = Enemy()
E4 = Enemy()
H = HGate()
PauliZ = PZGate()
PauliY = PYGate()
PauliX = PXGate()
Rx = RXGate()
Ry = RYGate()
Rz = RZGate()
cnot = CNOT()



#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
enemies.add(E2)
enemies.add(E3)
enemies.add(E4)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(E2)
all_sprites.add(E3)
all_sprites.add(E4)

gates = pygame.sprite.Group()
gates.add(H)
gates.add(PauliZ)
gates.add(PauliY)
gates.add(PauliX)
gates.add(Rx)
gates.add(Rz)
gates.add(Ry)

scoreGates = pygame.sprite.Group()
gates.add(cnot)

def drawMaze(surface):
    what_to_draw = {'H': 'H', 'Z': 'Z', 'X': 'X', 'Y': 'Y', 'RX': 'RX', 'RY': 'RY', 'RZ': 'RZ'}
    for row_id, row in enumerate(tiles):
        for col_id, col in enumerate(row):
            if col == 0:
                pygame.draw.rect(surface, WHITE, pygame.Rect(50*col_id, 50*row_id, 50, 50))
            elif col == 1:
                continue
            else:
                txt = pygame.font.Font.render(game_font, what_to_draw[col], True, WHITE)
                surface.blit(txt, (50*col_id + 15, 50*row_id + 10))

def die():
    DISPLAYSURF.fill(RED)
    pygame.display.update()
    for entity in all_sprites:
        entity.kill() 
    time.sleep(2)
    pygame.quit()
    sys.exit()


while True:
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    P1.update()

    for enemy in enemies:
        enemy.move()
     
    DISPLAYSURF.fill(BLACK)
    drawMaze(DISPLAYSURF)
    for entity in all_sprites:
        entity.draw(DISPLAYSURF)

    if pygame.sprite.spritecollideany(P1, enemies):
        if P1.is_collided_with(E1):
            verAlive = execute_measurement(P1.qGates, simulator, playerCircuit, quantumRotDict, quantumGateDict, "Z")
            if verAlive == 0:   
                die()
            else: 
                continue
        elif P1.is_collided_with(E2):
            verAlive = execute_measurement(P1.qGates, simulator, playerCircuit, quantumRotDict, quantumGateDict, "Z")
            if verAlive == 0:   
                die()
            else: 
                continue
        elif P1.is_collided_with(E3):
            verAlive = execute_measurement(P1.qGates, simulator, playerCircuit, quantumRotDict, quantumGateDict, "Y")
            if verAlive == 0:   
                die()
            else: 
                continue
        elif P1.is_collided_with(E4):
            verAlive = execute_measurement(P1.qGates, simulator, playerCircuit, quantumRotDict, quantumGateDict, "X")
            if verAlive == 0:   
                die()
            else: 
                continue
    
    if pygame.sprite.spritecollideany(P1, gates):
        if P1.is_collided_with(H):
            P1.qGates.append("Hadamard")
        elif P1.is_collided_with(PauliZ):
            P1.qGates.append("PauliZ")
        elif P1.is_collided_with(PauliX):
            P1.qGates.append("PauliX")
        elif P1.is_collided_with(PauliY):
            P1.qGates.append("PauliY")


    pygame.display.update()
    frame += 1
    frame = frame % 4
    FramePerSec.tick(FPS)
