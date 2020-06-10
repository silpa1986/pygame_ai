import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent single alien in fleet."""

    def __init__(self,ai_game):
        """Initialise the alien and set its starting position"""
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings


        #load the alien image and set its rect attribute.
        self.image=pygame.image.load('images/alien.bmp')
        self.rect=self.image.get_rect()

        #start the new alien near top left of screen.
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height

        #store the alie exact horizantal position.
        self.x=float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at its edge of screen."""
        screen_rect=self.screen.get_rect()
        if self.rect.right>=screen_rect.right or self.rect.left<=0:
            return True

    def update(self):
        """Move alien to the right or left"""
        self.x+=(self.settings.alien_speed*
                 self.settings.fleet_direction)
        
        self.rect.x=self.x
