import pygame
import random
from time import time
pygame.init()
width = 1000 # window width
height = 650 # window height
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('space_invaders')
red = (255, 0, 0)
green = (0, 255, 0)
text = pygame.font.SysFont("Helvetica", 20)


class Player:
    """
    This Class Controls and contains all the attributes of the player in the Game 
    The Player is composed of two different rect classes when it's drawn on screen.
    """
    x = 500 # The x coordinate of the bottom rect
    y = 550 # The y coordinate of the bottom rect
    vel = 5 # Player speed
    lives = 3
    head_x = x + 15 # The x coordinate of the top rect
    head_y = y - 10 # The y coordinate of the top rect
    bullets = []
    game_over = False
    won = False # Boolean that stores if the Player won or not after game over
    score = 0
    time_died = 0
    dead_img = pygame.image.load('dead_player.png').convert_alpha() # Image to display after Player dies
    dead = False
    was_hit = False  # Boolean that stores if the Player was hit by an Invader bullet or not
    animation_start = 0  # The time the animation of the Player starts when Player.was_hit is True
    color = 255      # Stores the part of the Player Rects color that needs to be increased or decreased during animation
    animation_inc = -25  # Increment/Decrement of the color variable during animation

    @staticmethod
    def render():
        """Renders the player on the screen"""
        Player.head_x = Player.x + 15
        Player.head_y = Player.y - 10
        if Player.was_hit:
            Player.render_as_blinking() # Start Blinking Animation
            return
        pygame.draw.rect(win, (0, Player.color, 0), (Player.head_x, Player.head_y, 10, 10))
        pygame.draw.rect(win, (0, Player.color, 0), (Player.x, Player.y, 40, 10))

    @staticmethod
    def render_as_blinking():
        """Animates the Player to be blinking on screen for 3 seconds"""
        pygame.draw.rect(win, (0, Player.color, 0), (Player.x, Player.y, 40, 10))
        pygame.draw.rect(win, (0, Player.color, 0), (Player.head_x, Player.head_y, 10, 10))

        # Increase or decrease Player.color during animation. We are animating Player.color 
        Player.color += Player.animation_inc

        if time() - Player.animation_start < 3: # If animation hasn't lasted 3 seconds
            if Player.color == 255: # Highest point of animation. Player.color can't be more than 255
                Player.animation_inc = -25
            elif Player.color == 30: # Lowest point of animation. We don't want Player.color to become black
                Player.animation_inc = 25
        else: # reset to defaults
            Player.was_hit = False
            Player.animation_start = 0
            Player.animation_inc = -25
            Player.color = 255

    @staticmethod
    def move():
        """
        Moves the player by increasing or decreasing the x coordinates when 
        the left or right arrow keys on the keyboard are presssed 
        """
        keys = pygame.key.get_pressed()

        if Player.x > 0: 
        # if the player hasn't reached the left edge of the screen
            if keys[pygame.K_LEFT]:
                Player.x -= Player.vel

        if Player.x + 40 < 1000:
        # if the player hasn't reached the right edge of the screen
            if keys[pygame.K_RIGHT]:
                Player.x += Player.vel

    @staticmethod
    def create_bullets():
        """ 
        Stores a list containing the coordinates of a bullet in 
        Player.bullets whenever the space key is pressed on the keyboard 
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            bullet_pos = [Player.head_x + 2, Player.head_y - 5]
            if len(Player.bullets) < 1:
                Player.bullets.append(bullet_pos)

            elif len(Player.bullets) >= 1:
                if Player.head_y >= Player.bullets[-1][1] + 100:
                # This allows bullets to be at a certain distance from each other when moving
                    Player.bullets.append(bullet_pos)

    @staticmethod
    def shoot():
        """Renders and Moves each bullet in the Player.bullets list towards the direction of the Invaders"""
        for bullet in Player.bullets:
            pygame.draw.rect(win, green, (bullet[0], bullet[1], 5, 20))
            bullet[1] -= 10
            if bullet[1] <= 0: 
                Player.bullets.remove(bullet)

    @staticmethod
    def explode():
        """Renders the player as if it exploded"""
        if time() - Player.time_died < 0.3:
            # Display dead Player sprite
            win.blit(Player.dead_img, (Player.x, Player.head_y)) 
        else:
            # If the dead Player sprite has beed displayed for 0.3 seconds
            Player.game_over = True
            Player.won = False

class Invaders:
    """ 
    This Class controls and contains all the attributes of every invader in the Game 
    There are 44 Invaders in total divided into 4 rows and 11 columns when rendered 
    """
    vel_x = 5   # Horizontal speed of each invader in the game. It will change frequently during the game
    vel_y = 5   # Vertical speed of each invader in the game. It is constant
    width = 40    # Width of each Invader
    height = 40   # Height of each Invader
    dead_invader = pygame.image.load('dead_invader.png').convert_alpha() # Dead invader sprite

    # Stores coordinates of invaders that are allowed to shoot. There are no invaders in front
    # of them when rendered So they can't shoot other Invaders, only the Player.
    invaders_that_can_shoot = []

    bullets = [] # Stores bullet coordinates for the invaders
    all_invaders_are_dead = False
    coordinates = []
    last_left = []
    last_right = []

    @staticmethod
    def init_invaders_properties():
        """Sets the default values for Invaders properties"""

        # The first and second items in each of the nested lists stores the x and y positions respectively
        # while the third item stores the column at which the invader is located.
        Invaders.coordinates = [[115, 20, 0], [185, 20, 1], [255, 20, 2], [325, 20, 3], [395, 20, 4], [465, 20, 5], [535, 20, 6], [605, 20, 7], [675, 20, 8], [745, 20, 9], [815, 20, 10],
                       [115, 80, 0], [185, 80, 1], [255, 80, 2], [325, 80, 3], [395, 80, 4], [465, 80, 5], [535, 80, 6], [605, 80, 7], [675, 80, 8], [745, 80, 9], [815, 80, 10],
                       [115, 140, 0], [185, 140, 1], [255, 140, 2], [325, 140, 3], [395, 140, 4], [465, 140, 5], [535, 140, 6], [605, 140, 7], [675, 140, 8], [745, 140, 9], [815, 140, 10],
                       [115, 200, 0], [185, 200, 1], [255, 200, 2], [325, 200, 3], [395, 200, 4], [465, 200, 5], [535, 200, 6], [605, 200, 7], [675, 200, 8], [745, 200, 9], [815, 200, 10]]

        Invaders.last_left = Invaders.coordinates[33] # Last invader in the first column of invaders when rendered. Used to detect collision with walls
        Invaders.last_right = Invaders.coordinates[-1] # Last invader in the last column of invaders when rendered. Used to detect collision with walls
        Invaders.invaders_that_can_shoot = []
        Invaders.vel_x = 5
        Invaders.bullets = []
   
        for i in range(33, 44):
            Invaders.invaders_that_can_shoot.append(Invaders.coordinates[i]) # Last row of invaders when rendered from top to bottom

    @staticmethod
    def render_invaders():
        """Renders each invader in Invaders.coordinates list on screen"""
        for coordinate in Invaders.coordinates:
            if coordinate:
                if coordinate[2] >= 0: # If invader is not set to be displayed as dead
                    pygame.draw.rect(win, red, (coordinate[0], coordinate[1], Invaders.width, Invaders.height)) # Draws the invader
                    pygame.draw.rect(win, (20, 20, 20), (coordinate[0]+15, coordinate[1]+30, 10, 10)) # This is just a design on each invader
                elif time() - coordinate[3] < 0.2: # If invader is set to be displayed as dead
                    win.blit(Invaders.dead_invader, (coordinate[0], coordinate[1]))
                else:
                    # Stops the Invader from being rendered at all
                    coordinate = None

    @staticmethod
    def check_for_collision_with_walls():
        """Uses the last_right and last_left variables to detect invaders collisions with walls"""
        move_invaders_down = False

        if Invaders.vel_x > 0: # If invaders are moving right
            if Invaders.last_right[0] + Invaders.width >= 1000:
            # If the invader has collided with the wall on the right in the game
                Invaders.vel_x = -5
                move_invaders_down = True

        elif Invaders.vel_x < 0: # If invaders are moving left
            if Invaders.last_left[0] <= 0:
            # If the invader has collided with the wall on the left in the game
                Invaders.vel_x = 5
                move_invaders_down = True

        if move_invaders_down:
            for coordinate in Invaders.coordinates:
                if coordinate:
                    coordinate[1] += Invaders.vel_y

    @staticmethod
    def move_invaders():
        """ 
        Increases the x coordinate of each invader; Causing it to move when it's being rendered and 
        updates the last_right and last_left variables incase the invaders they stored has been killed
        """
        Invaders.all_invaders_are_dead = True

        # The x and y coordinates of both variables will be updated later
        Invaders.last_right = [0, 0, 0] # Sets the column value to the lowest value; the first column when rendered
        Invaders.last_left = [0, 0, 10] # Sets the column value to the highest value; the last column when rendered

        for coordinate in Invaders.coordinates:
            if not coordinate:
                continue

            # If the invader hasn't been killed yet
            if coordinate[2] >= 0:
                if Invaders.vel_x > 0: # If invaders are moving right
                    if coordinate[2] >= Invaders.last_right[2]:
                        Invaders.last_right = coordinate
                elif Invaders.vel_x < 0: # If invaders are moving left
                    if coordinate[2] <= Invaders.last_left[2]:
                        Invaders.last_left = coordinate

                # If the loop ends without ever executing this expression;
                # That means all invaders are dead
                Invaders.all_invaders_are_dead = False
            coordinate[0] += Invaders.vel_x # Moves the Invaders

            # Checks if an Invader has passed or is on the same plane as the Player
            if coordinate[1] + Invaders.height >= Player.head_y:
                Player.game_over = True
                Player.won = False

        if Invaders.all_invaders_are_dead:
           Player.game_over = True
           Player.won = True
           return
        Invaders.check_for_collision_with_walls()

    @staticmethod
    def create_bullets():
        """ 
        Create bullet coordinates for invaders by using the coordinates of the invaders
        present in the invaders_that_can_shoot list and adds it to the Invaders.bullets list
        """
        if not Invaders.all_invaders_are_dead:
            if len(Invaders.bullets) < 4:
                position = random.choice(Invaders.invaders_that_can_shoot)
                if len(Invaders.bullets) >= 1:
                    if (Invaders.bullets[-1][1] - 30) < position[1] + 40:
                        return # This allows bullets to be at a certain distance from each other when moving
                bullet = position.copy()
                bullet[0] += 20 # This will make the bullet come out of the centre of the invader when rendered
                bullet[1] += 20 # This will make the bullet come out of the centre of the invader when rendered
                bullet.pop(2)
                Invaders.bullets.append(bullet)

    @staticmethod
    def shoot_bullets():
        """Renders and Moves each bullet in the Invaders.bullets list towards the direction of the Player"""
        if Invaders.bullets:
            for bullet in Invaders.bullets:
                pygame.draw.rect(win, red, (bullet[0], bullet[1], 5, 20))
                bullet[1] += 10
                if bullet[1] + 20 >= 650: # if the bullet has left the screen
                    Invaders.bullets.remove(bullet)

    @staticmethod
    def update_invaders_that_can_shoot(invader_index):
        """ 
        Updates the invaders_that_can_shoot list anytime an invader is killed 
        if the invader killed is part of invaders_that_can_shoot list
        """
        replace_invader = False
        for invader in Invaders.invaders_that_can_shoot:
            if invader is Invaders.coordinates[invader_index]:
                Invaders.invaders_that_can_shoot.remove(invader)
                replace_invader = True
                break
        # Setting it as -1 marks it as a dead Invader. A dead Invader sprite will be rendered in it's position 
        Invaders.coordinates[invader_index][2] = -1 
        # The time appended will be used to get how long the dead Invader sprite has been displayed on screen
        Invaders.coordinates[invader_index].append(time()) 
        if not replace_invader:
            return      
        for i in range(4): # Since there are only 4 invaders in a column
            if invader_index <= 10:
            # The program has reached the index of the last invader in a column; all the invaders in that column are dead
                break
            # A dead invader in invaders_that_can_shoot list can only be replaced by an invader that's  
            # in the same column with it. Invaders on the same column have indexes that are apart by 11
            invader_index -= 11
            if Invaders.coordinates[invader_index][2] >= 0: # if the invader is not dead
                Invaders.invaders_that_can_shoot.append(Invaders.coordinates[invader_index])
                break

def display_game_over_msg():
    """Displays game over message"""
    pygame.draw.rect(win, (255, 255, 255), (350, 300, 300, 150))
    
    if Player.won:
        pygame.draw.rect(win, green, (350, 300, 300, 30))
        win.blit(text.render("You won! All invaders are dead.", True, (50, 50, 50)), (380, 360))
    else:
        pygame.draw.rect(win, red, (350, 300, 300, 30))
        win.blit(text.render("You Lost! The invaders defeated you.", True, (50, 50, 50)), (360, 360))
    win.blit(text.render("GAME OVER!", False, (50, 50, 50)), (430, 305))
    win.blit(text.render("Press P to play again!", True, (50, 50, 50)), (410, 380))

def player_shoots_invader():
    """Checks for collision between Player bullets and invaders"""
    for i in range(len(Invaders.coordinates)):
        if not Invaders.coordinates[i] or Invaders.coordinates[i][2] < 0:
            # If invader is dead
            continue
        for bullet in Player.bullets:
            if bullet[0] >= Invaders.coordinates[i][0] and bullet[0] + 5 <= Invaders.coordinates[i][0]+40:
                if bullet[1] <= Invaders.coordinates[i][1] + 40 and Invaders.coordinates[i][1] < bullet[1] + 20:
                    # If invader has been hit with a bullet from the Player
                    Invaders.update_invaders_that_can_shoot(i)
                    Player.bullets.remove(bullet)
                    Player.score += 1
                    break
                        
def invader_shoots_player():
    """Checks for collision between invaders bullets and Player"""
    if Player.was_hit:
        # Player can't be hit during Blinking animation
        return
    for shot in Invaders.bullets[:]:
        if shot[0] >= Player.head_x and shot[0] + 5 <= Player.head_x+10:
            if shot[1] + 20 >= Player.head_y and Player.head_y + 10 > shot[1]:
                # If invader bullet collides with the Player's head Rect
                Invaders.bullets.remove(shot)
                Player.lives -= 1
                Player.was_hit = True
                Player.animation_start = time()

        elif shot[0] >= Player.x and shot[0] + 5 <= Player.x+40:
            if shot[1] + 20 >= Player.y and Player.y + 10 > shot[1]:
                # If invader bullet collides with the Player's body Rect
                Invaders.bullets.remove(shot)
                Player.lives -= 1
                Player.was_hit = True
                Player.animation_start = time()

        if Player.lives == 0:
            Player.dead = True
            Player.time_died = time()

def reset_game():
    """Resets changed game values back to default"""
    Player.dead = False
    Player.game_over = False
    Player.won = False
    Player.x = 500 
    Player.y = 550
    Player.lives = 3
    Player.bullets = []
    Player.score = 0
    Player.time_died = 0
    Invaders.init_invaders_properties()
    print(Invaders.invaders_that_can_shoot)

Invaders.init_invaders_properties()
run = True
while run: # Main game loop
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    win.fill((20, 20, 20))
    win.blit(text.render("LIVES: " + str(Player.lives), True, (0, 255, 0)), (930, 5))
    win.blit( text.render("SCORE: " + str(Player.score), True, (0, 255, 0)), (5, 5))
    Invaders.render_invaders()
    if Player.dead:
        Player.explode()
    else:
        Player.render()
        
    if not Player.game_over:
        Invaders.move_invaders()
        Player.move()
        Invaders.create_bullets()
        Invaders.shoot_bullets()
        if not Player.was_hit: 
            # Player shouldn't create bullets during blinking animation 
            # but can shoot if the bullet has already been created before then
            Player.create_bullets()
        Player.shoot()
        player_shoots_invader()
        invader_shoots_player()
    else:
        display_game_over_msg()
        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_p]:
            reset_game()

    pygame.display.update()

pygame.quit()