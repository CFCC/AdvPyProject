import pygame
import random
from block import Block
from goodBlock import GoodBlock

# Define some colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
BLUE = (0,   0,   255)
GREEN = (0,   255,   0)
 

class Player(pygame.sprite.Sprite):
    """ The class is the player-controlled sprite. """
 
    # -- Methods
    def __init__(self, x, y):
        """Constructor function"""
        # Call the parent's constructor
        super().__init__()
 
        # Set height, width
        self.image = pygame.Surface([15, 15])
        self.image.fill(BLUE)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
        # -- Attributes
        # Set speed vector
        self.change_x = 0
        self.change_y = 0
 
    def changespeed(self, x, y):
        """ Change the speed of the player"""
        self.change_x += x
        self.change_y += y
 
    def update(self):
        """ Find a new position for the player"""
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        if self.rect.x < 0:
            bump.play()
            self.rect.x = 0
        if self.rect.x > 685:
            bump.play()
            self.rect.x = 685
        if self.rect.y < 0:
            bump.play()
            self.rect.y = 0
        if self.rect.y > 385:
            bump.play()
            self.rect.y = 385
# Initialize Pygame
pygame.init()

bump = pygame.mixer.Sound("bump.wav")
# Set the height and width of the screen
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])
 
# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
good_block_list = pygame.sprite.Group()
bad_block_list = pygame.sprite.Group()
 
# This is a list of every sprite. 
# All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()
 
for i in range(50):
    # This represents a block
    block = GoodBlock(GREEN, 15, 15)
 
    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height)
 
    # Add the block to the list of objects
    good_block_list.add(block)
    all_sprites_list.add(block)

for i in range(50):
    # This represents a block
    block = Block(RED, 15, 15)
 
    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height)
 
    # Add the block to the list of objects
    bad_block_list.add(block)
    all_sprites_list.add(block)
 
# Create a RED player block
player = Player(10, 10)
all_sprites_list.add(player)
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
score = 0
good_sound = pygame.mixer.Sound("good_block.wav")
bad_sound = pygame.mixer.Sound("bad_block.wav")
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True
        # Set the speed based on the key pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-1, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(1, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, -1)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, 1)
        # Reset speed when key goes up
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(1, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-1, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, 1)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, -1)
    all_sprites_list.update() 
    # Clear the screen
    screen.fill(WHITE)
 
    # See if the player block has collided with anything.
    good_blocks_hit_list = pygame.sprite.spritecollide(player, good_block_list, True)
    bad_blocks_hit_list = pygame.sprite.spritecollide(player, bad_block_list, True)
    # Check the list of collisions.
    for block in good_blocks_hit_list:
        score += 1
        good_sound.play()
    for block in bad_blocks_hit_list:
        score -= 1
        bad_sound.play()
    # Draw all the spites
    all_sprites_list.draw(screen)
    # Select the font to use, size, bold, italics
    font = pygame.font.SysFont('Verdana', 25, False, False)
 
    # Render the text. "True" means anti-aliased text.
    # Black is the color. The variable BLACK was defined
    # above as a list of [0, 0, 0]
    # Note: This line creates an image of the letters,
    # but does not put it on the screen yet.
    text = font.render("Score: " + str(score),True,BLACK)
 
    # Put the image of the text on the screen at 250x250
    screen.blit(text, [10, 10])
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit to 60 frames per second
    clock.tick(60)
 
pygame.quit()