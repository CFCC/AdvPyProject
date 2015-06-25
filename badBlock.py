from block import Block
import pygame
import random
class BadBlock(Block):
    """
    This class represents the ball.
    It derives from the "Sprite" class in Pygame.
    """
    def update(self):
        """ Find a new position for the player"""
        self.rect.x += random.randint(-3,3) 
        self.rect.y += random.randint(-3,3) 