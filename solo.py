import pygame
 
# Global constants
moving_pfy1 = 700
pfy_change = 1

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PORTAL = (255, 84 ,205)
INVISIBLE = (250,250,250)
 
# Screen dimensions
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
 
 
class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """
 
    # -- Methods
    def __init__(self):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 60
        self.image = pygame.image.load("stick.png").convert()
        self.image.set_colorkey(WHITE)
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None
 
    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
                
        block_hit_list = pygame.sprite.spritecollide(self, self.level.moving_platform, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
        enemy_block_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)

        for block in enemy_block_hit_list:
            self.rect.y = 40
            self.rect.x = 40
        
        
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
        block_hit_list = pygame.sprite.spritecollide(self, self.level.moving_platform, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0




 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = 40
            self.rect.x = 40
            
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        moving_platform_hit_list = pygame.sprite.spritecollide(self, self.level.moving_platform, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or len(moving_platform_hit_list) or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
            
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
 
 
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
 
        self.rect = self.image.get_rect()
        
        
class Moving_Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height, direction, start, end, speed):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
 
        self.rect = self.image.get_rect()
        self.direction = direction
        self.end = end
        self.start = start
        self.speed = speed
    def update(self):
        if self.direction.lower() == "x":
            self.rect.x += self.speed
            if self.rect.x == self.end:
                self.speed = self.speed*-1
            elif self.rect.x == self.start:
                self.speed = self.speed*-1
        if self.direction.lower() == "y":
            self.rect.y += self.speed
            if self.rect.y == self.end:
                self.speed = self.speed*-1
            elif self.rect.y == self.start:
                self.speed = self.speed*-1
            
        
        
class Enemy(pygame.sprite.Sprite):
    """ ENEMY """
 
    def __init__(self, width, height):
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
 
        self.rect = self.image.get_rect() 
 
class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.moving_platform = pygame.sprite.Group()
        self.player = player
         
        # Background image
        self.background = pygame.image.load("towerwall.png").convert()
 
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
        self.moving_platform.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        screen.blit(self.background, [0, 0])
        
        
        
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.moving_platform.draw(screen)
 
 
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        # Array with width, height, x, and y of platform
        level = [[210, 10, 0, 100],
                 [210, 10, 200, 600],
                 [210, 10, 590, 500],
                 [210, 10, 800, 350],
                 [210, 10, 1165, 200],
                 ]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        level = []    
        
        #width, height, x, y, "x" or "y", start(same as x), end, speed         

        for platform in level:
            block = Moving_Platform(platform[0], platform[1],platform[4], platform[5], platform[6],platform[7])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.moving_platform.add(block)
            
class Level_02(Level):
    """ Definition for level 1. """
     
    def __init__(self, player):
        """ Create level 1. """
     
            # Call the parent constructor
        Level.__init__(self, player)
     
            # Array with width, height, x, and y of platform
        level = [[1100, 10, 0, 350],
                 [55, 5, 200, 220],
                 [55, 5, 400, 220],
                 [55, 5, 600, 220],
                 [55, 5, 800, 220],
                 [150, 10, 1216, 600],
                 [50, 10, 350, 700],
                 [50, 10, 250, 600],
                 [50, 10, 150, 500],
                    ]
     
            # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

            
        level = [[900,15, 200, 335]
                 ]

        for platform in level:
            block = Enemy(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.enemy_list.add(block)

        #width, height, x, y, "x" or "y", start(same as x), end, speed
        level = [[250, 10 ,650, 700, "y", 700, 350, -1]]
        
            
        for platform in level:
            block = Moving_Platform(platform[0], platform[1],platform[4], platform[5], platform[6],platform[7])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.moving_platform.add(block)

            
        # Go through the array above and add platforms
class Level_03(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        # Array with width, height, x, and y of platform
        level = [[210, 10, 0, 150],
                 [210, 1, 1000, 600],
                 [210, 1, 400, 400],
                 [210, 1, 800, 350],
                 [210, 1, 1100, 500],
                 [10, 300, 210, 150],
                 [100, 1, 0, 600],]
                 
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

    
        #SLPIT
    
        level = [[210, 10, 600, 600,"x",1100, 0, 1]]
        #width, height, x, y, "x" or "y", start(same as x), end, speed         

        for platform in level:
            block = Moving_Platform(platform[0], platform[1],platform[4], platform[5], platform[6],platform[7])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.moving_platform.add(block)

        level = [[900, 15, 150, 500]
                 ]

        for platform in level:
            block = Enemy(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.enemy_list.add(block)
        

class Level_04(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        # Array with width, height, x, and y of platform
        level = [[100, 1, 500, 200],
                 [100, 1, 800, 600],
                 [100, 1, 380, 500],
                 [100, 1, 800, 350],
                 [100, 1, 1100, 500],
                 [100, 4, 0, 600],
                 [100, 1, 175, 125],]
                 
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
class Level_05(Level): 
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        # Array with width, height, x, and y of platform
        level = [[210, 10, 0, 700],
                 [210, 10, 210, 600],
                 [210, 10, 420, 500],
                 [210, 10, 630, 400],
                 [210, 10, 840, 300],
                 [1156, 100, 210, 610],
                 [946, 100, 420, 510],
                 [420, 100, 630, 410],
                 [210, 100, 840, 310],
                 ]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        
        level = [[190, 50, 230, 550],
                 [190, 50, 440, 450],
                 [190, 50, 650, 350],
                 ]

        for platform in level:
            block = Enemy(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.enemy_list.add(block)
def main():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
 
    pygame.display.set_caption("Platformer Jumper")
 
    # Create the player
    player = Player()
 
    # Create all the levels
    level_list = []
    level_list.append( Level_01(player) )
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    level_counter = 1
    player.rect.x = 40
    player.rect.y = 40
    active_sprite_list.add(player)
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    font = pygame.font.Font(None, 25)
    frame_count = 0
    frame_rate = 60
    start_time = 90
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_a:
                    player.go_left()
                if event.key == pygame.K_d:
                    player.go_right()
                if event.key == pygame.K_w:
                    player.jump()
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_d and player.change_x > 0:
                    player.stop()
        if player.rect.x >= 1340 and player.rect.y <= 200 and level_counter == 1:
           level_list = []
           level_list.append( Level_02(player) )
           current_level_no = 0
           current_level = level_list[current_level_no]
           player.level = current_level
           player.rect.x = 20
           player.rect.y = 200
           level_counter += 1
           
        if player.rect.x >= 0 and player.rect.y >= 349 and  player.rect.x <=149 and level_counter == 2:
           level_list = []
           level_list.append( Level_03(player) )
           current_level_no = 0
           current_level = level_list[current_level_no]
           player.level = current_level
           player.rect.x = 20
           player.rect.y = 40
           level_counter += 1
           
        if player.rect.x >= 0 and player.rect.y >= 349 and  player.rect.x <=149 and level_counter == 3:
           level_list = []
           level_list.append( Level_04(player) )
           current_level_no = 0
           current_level = level_list[current_level_no]
           player.level = current_level
           player.rect.x = 20
           player.rect.y = 500
           level_counter += 1
           
        if player.rect.x <= 175 and player.rect.y <= 0 and level_counter == 4:
           level_list = []
           level_list.append( Level_05(player) )
           current_level_no = 0
           current_level = level_list[current_level_no]
           player.level = current_level
           player.rect.x = 20
           player.rect.y = 500
           level_counter += 1   
        # Update the player.
        active_sprite_list.update()
 
        # Update items in the level
        current_level.update()
 
        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH
 
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left < 0:
            player.rect.left = 0
 
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        total_seconds = frame_count // frame_rate
 
        # Divide by 60 to get total minutes
        minutes = total_seconds // 60
 
        # Use modulus (remainder) to get seconds
        seconds = total_seconds % 60
 
        # Use python string formatting to format in leading zeros
        output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)
 
        # Blit to the screen
        text = font.render(output_string, True, BLACK)
        screen.blit(text, [15, 740])
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        frame_count += 1
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
 
if __name__ == "__main__":
    main()

