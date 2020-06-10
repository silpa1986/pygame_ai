import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
class AlienInvasion:
    """overall class to manage game assets and behaviour"""
    def __init__(self):
        """initialise the game , and create game resourses"""
        pygame.init()
        self.settings=Settings()
        
        
        
        self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("AlienInvasion")
        self.ship=Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        """start the main loop for the game"""
        while True:
            self._check_events()
            self.ship.update()
            
            self._update_bullets()
            self._update_aliens()
                   
                
            self._update_screen()
    def _check_events(self):
        """respond to key presses and mouse events"""
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)
                
    def _check_keydown_events(self,event):
        """respond to keypresses"""
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=True
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=True
        elif event.key==pygame.K_q:
            sys.exit()
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()
    def _check_keyup_events(self,event):
        """Respond to key releases"""
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=False

    def _fire_bullet(self):
        """Create a new bullet and add it to group of bullets"""
        if len(self.bullets)<self.settings.bullets_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)
    def _update_bullets(self):
        """update position of bullets get rid of old bullet"""
        #update bullate positions.
        self.bullets.update()

        #Get rid of old bullets.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)

    def _create_fleet(self):
        """create the fleet of aliens"""
        #Create an alien and find the number of aliens in a row.
        #spacing between each alien is equal to one alien width.
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        available_space_x=self.settings.screen_width-(2*alien_width)
        number_aliens_x=available_space_x//(2*alien_width)
        #determine the number of rows that fit on the screen.
        ship_height=self.ship.rect.height
        available_space_y=(self.settings.screen_height-
                           (3*alien_height)-ship_height)
        number_rows=available_space_y//(2*alien_height)
        #create full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)
                
                           
        

    def _create_alien(self,alien_number,row_number):
        """create an alien and place it in the row."""
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        alien.x=alien_width+2*alien_width*alien_number
        alien.rect.x=alien.x
        alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleets's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction=-1    
                
      
    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
         then update the positions of all aliens in a fleet
        """
        self._check_fleet_edges()

        self.aliens.update()

    def _update_screen(self):
        """update images on screen and flip to new screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)    
        """make the most recently drawn screen visible"""
        pygame.display.flip()
            
if __name__=='__main__':
    """make a game instance,and run a game"""
    ai=AlienInvasion()
    ai.run_game()
    
