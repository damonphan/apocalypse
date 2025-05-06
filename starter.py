import pygame
from pygame.locals import *
import os
import sys
import math
import random

pygame.init()
#Screen setup
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Apocalypse Project')

#clock
clock = pygame.time.Clock()
fps = 60

#background image
bg_img = pygame.image.load('images/bg.png')
bg_scaled = pygame.transform.scale(bg_img, (screen_width, screen_height))


#colors
Gray = (141, 149, 161)

#Tile Size
tile_size = 40

#ground images
ground_img = pygame.image.load("images/ground.png")
ground_img = pygame.transform.scale(ground_img, (tile_size, tile_size))

#overlay for newspaper and flag
newspaper_overlay = pygame.image.load("images/newspaper_overlay.png")
newspaper_overlay = pygame.transform.scale(newspaper_overlay, (screen_width, screen_height))

show_overlay = False
newspaper_read = False
computer_object = None

#ground position
ground_y = screen_height - tile_size

#npc initialize
john_npc = None

#player class
class Player():
    def __init__(self, x, y):
        self.images_right = [
            pygame.image.load('images/walk_1.png'),
            pygame.image.load('images/walk_2.png')

        ]
        self.images_left = [
            pygame.transform.flip(images,True,False) for images in self.images_right

        ]
        self.index = 0
        self.counter = 0
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = ground_y - self.rect.height  # <-- Align bottom of player with top of ground
        self.direction = 1  # 1 = right, -1 = left
        self.can_move = True

    def update(self, ground_object=None):
        dx = 0
        walk_speed = 3
        walk_cooldown = 10
        key = pygame.key.get_pressed()

        if self.can_move:
            if key[pygame.K_LEFT]:
                dx = -walk_speed
                self.direction = -1
                self.counter += 1
            elif key[pygame.K_RIGHT]:
                dx = walk_speed
                self.direction = 1
                self.counter += 1
            else:
                self.counter = 0
                self.index = 0

        # Animate
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index = (self.index + 1) % 2  # Only 2 frames
            if self.direction == 1:
                self.image = self.images_right[self.index]
            else:
                self.image = self.images_left[self.index]

        # If standing still, set first frame
        if dx == 0:
            if self.direction == 1:
                self.image = self.images_right[0]
            else:
                self.image = self.images_left[0]

        self.rect.x += dx
        screen.blit(self.image, self.rect)

        # Only check collision if object exists
        if ground_object and self.rect.colliderect(ground_object.rect) and not newspaper_read:
            self.can_move = False




    def reset(self):
        self.can_move = True
        # self.rect.x = 100  # Reset player's position
        # self.rect.y = ground_y - self.rect.height  # Reset player to ground level


class Game:
    def __init__(self):
        self.screen_state = "game"  # Current screen state (e.g., 'game', 'level_end')
        self.bg_img = pygame.image.load('images/bg.png')  # Initial background
        self.bg_scaled = pygame.transform.scale(self.bg_img, (screen_width, screen_height))

        self.bg_2_img = pygame.image.load('images/bg_2.png')  # New background for the next level
        self.bg_2_scaled = pygame.transform.scale(self.bg_2_img, (screen_width, screen_height))

        self.bg_3_img = pygame.image.load('images/bg_3.png')  # New background for the next level
        self.bg_3_scaled = pygame.transform.scale(self.bg_3_img, (screen_width, screen_height))

        self.bg_4_img = pygame.image.load('images/bg_4.png')  # New background for the next level
        self.bg_4_scaled = pygame.transform.scale(self.bg_4_img, (screen_width, screen_height))

        self.bg_5_img = pygame.image.load('images/bg_5.png')  # New background for the next level
        self.bg_5_scaled = pygame.transform.scale(self.bg_5_img, (screen_width, screen_height))

        self.level = 1

    def update(self, player):
        if player.rect.x > screen_width:  # Check if player reaches the end of the screen
            self.change_screen()
            player.rect.x = 100
    
    def change_screen(self):
        self.level += 1
        if self.level == 2:
            self.screen_state = "level_2"
        elif self.level == 3:
            self.screen_state = "level_3"
        elif self.level == 4:
            self.screen_state = "level_4"
        elif self.level == 5:
            self.screen_state = "level_5"


    def get_background(self):
        if self.screen_state == "game":
            return self.bg_scaled
        elif self.screen_state == "level_2":
            return self.bg_2_scaled
        elif self.screen_state == "level_3":
            return self.bg_3_scaled
        elif self.screen_state == "level_4":
            return self.bg_4_scaled
        elif self.screen_state == "level_5":
            return self.bg_5_scaled
    
    def reset(self):
        # Reset player position and level objects for the new level
        player.rect.x = 100  # Reset player's position
        player.rect.y = ground_y - player.rect.height  # Reset player to ground level
        # Reset other objects (e.g., enemies, obstacles, etc.)

# Create a simple object to add to the ground
class GroundObject():
    def __init__(self, x, y):
        self.image = pygame.image.load("images/waste.png")
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self):
        screen.blit(self.image, self.rect)

class NPC:
    def __init__(self, x, y):
        self.image = pygame.image.load("images/john.png")
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size * 2))  # Taller NPC
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        self.dialogue_options = [
            "I had a dream about this day.",
            "Have you been chipped yet?",
            "It's been so long since I've seen flesh and blood around here.",
            "You're not supposed to be this far. Hide before it sees you."
        ]
        self.dialogue_font = pygame.font.SysFont('Arial', 20)
        self.dialogue_surface = None
    def draw(self):
        screen.blit(self.image, self.rect)
        if self.clicked and self.dialogue_surface:
            screen.blit(self.dialogue_surface, (self.rect.x - 20, self.rect.y - 40))
    def interact(self):
        if not self.clicked:
            self.clicked = True
            dialogue_text = random.choice(self.dialogue_options)
            self.dialogue_surface = self.dialogue_font.render(dialogue_text, True, (3, 23, 252))
class ComputerObject:
    def __init__(self, x, y):
        self.image = pygame.image.load("images/computer.png")
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self):
        screen.blit(self.image, self.rect)




computer_object = ComputerObject(200, ground_y - tile_size)
game = Game()
player = Player(100, 0)
ground_object = GroundObject(400, ground_y - tile_size)  # Add object at some point on the ground

run = True
while run:
    clock.tick(fps)

    screen.blit(game.get_background(), (0, 0))


    # Draw ground
    for x in range(0, screen_width, tile_size):
        screen.blit(ground_img, (x, ground_y))
    
    # Update player
    if game.screen_state == "level_2":
        player.update(ground_object)
    elif game.screen_state == "level_4":
        player.update(john_npc if john_npc and not john_npc.clicked else None)
    else:
        player.update(None)


    
    # Update game state
    game.update(player)  # Check if the player has reached the end
    
    if game.screen_state == "level_2" and not newspaper_read:
        # Show level end screen or new screen (reset, load new objects)
        ground_object.draw()  # Add the object to the new screen
    
    if game.screen_state == "level_4" and john_npc:
        john_npc.draw()
    if game.screen_state == "level_5":
        if computer_object is None:
            computer_object = ComputerObject(200, ground_y - tile_size)
        computer_object.draw()


    if show_overlay:
        screen.blit(newspaper_overlay, (0, 0))
    pygame.display.update()

    if game.screen_state == "level_4" and john_npc is None:
        john_npc = NPC(300, ground_y - tile_size * 2)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if show_overlay:
                # Close overlay
                show_overlay = False
                player.can_move = True
                newspaper_read = True

            elif not show_overlay and game.screen_state == "level_2" and not newspaper_read:
                if ground_object.rect.collidepoint(event.pos):
                    show_overlay = True
                    player.can_move = False

            elif game.screen_state == "level_4" and john_npc and john_npc.rect.collidepoint(event.pos):
                john_npc.interact()
                player.can_move = True
            elif game.screen_state == "level_5" and computer_object and computer_object.rect.collidepoint(event.pos):
                import subprocess
                subprocess.Popen([sys.executable, "demo.py"])


    


pygame.quit()


