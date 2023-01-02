import pygame
import random
pygame.init()
width = 1000
height = 650
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('space_invaders')
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
selection = [390, 190]
text = pygame.font.SysFont("Helvetica", 20)
score = 0
run = True

class Player:
    """
    This Class Controls and contains everything related to the player in the Game
    The Player is composed of two different rect classes when it's drawn on screen.
    """
    x = 500 # The x coordinate of the bottom rect
    y = 550 # The y coordinate of the bottom rect
    vel = 5 # Player speed
    lives = 3
    head_x = x + 15 # The x coordinate of the top rect
    head_y = y - 10 # The y coordinate of the top rect
    bullets = []

    @staticmethod
    def refresh():
        """Draws the player on the screen"""
        Player.head_x = Player.x + 15
        Player.head_y = Player.y - 10
        pygame.draw.rect(win, green, (Player.x, Player.y, 40, 10))
        pygame.draw.rect(win, green, (Player.head_x, Player.head_y, 10, 10))

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
        Player.bullets when the space key is pressed on the keyboard 
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            bullet_pos = [Player.head_x + 2, Player.head_y - 5]
            if len(Player.bullets) < 1:
                Player.bullets.append(bullet_pos)

            elif len(Player.bullets) >= 1:
                if Player.head_y >= Player.bullets[-1][1] + 100:
                # This allows bullets to be at a certain distance from each other 
                    Player.bullets.append(bullet_pos)

    @staticmethod
    def shoot():
        """ Draws and increases the y coordinate of every bullet found in Player.bullets """
        for bullet in Player.bullets:
            pygame.draw.rect(win, green, (bullet[0], bullet[1], 5, 20))
            bullet[1] -= 10
            if bullet[1] <= 0: 
                Player.bullets.remove(bullet)

class Invaders:
    vel_x = 5
    vel_y = 5
    width = 40
    height = 40
    invaders_that_can_shoot = []
    bullets = []
    all_invaders_are_dead = False
    coordinates = [[115, 20, 0], [185, 20, 1], [255, 20, 2], [325, 20, 3], [395, 20, 4], [465, 20, 5], [535, 20, 6], [605, 20, 7], [675, 20, 8], [745, 20, 9], [815, 20, 10],
                        [115, 80, 0], [185, 80, 1], [255, 80, 2], [325, 80, 3], [395, 80, 4], [465, 80, 5], [535, 80, 6], [605, 80, 7], [675, 80, 8], [745, 80, 9], [815, 80, 10],
                        [115, 140, 0], [185, 140, 1], [255, 140, 2], [325, 140, 3], [395, 140, 4], [465, 140, 5], [535, 140, 6], [605, 140, 7], [675, 140, 8], [745, 140, 9], [815, 140, 10],
                        [115, 200, 0], [185, 200, 1], [255, 200, 2], [325, 200, 3], [395, 200, 4], [465, 200, 5], [535, 200, 6], [605, 200, 7], [675, 200, 8], [745, 200, 9], [815, 200, 10]]
    last_left =  coordinates[33]
    last_right = coordinates[-1]

    for i in range(33, 44):
        invaders_that_can_shoot.append(coordinates[i])

    @staticmethod
    def create_invaders():
        for coordinate in Invaders.coordinates:
            if coordinate:
                pygame.draw.rect(win, red, (coordinate[0], coordinate[1], Invaders.width, Invaders.height))

    @staticmethod
    def check_for_collision_with_walls():
        move_invaders_down = False

        if Invaders.vel_x > 0:
            if Invaders.last_right[0] + Invaders.width >= 1000:
                Invaders.vel_x = -5
                move_invaders_down = True

        elif Invaders.vel_x < 0:
            if Invaders.last_left[0] <= 0:
                Invaders.vel_x = 5
                move_invaders_down = True

        if move_invaders_down:
            for coordinate in Invaders.coordinates:
                if coordinate:
                    coordinate[1] += Invaders.vel_y

    @staticmethod
    def move_invaders():
        Invaders.all_invaders_are_dead = True
        Invaders.last_right = [0, 0, 0]
        Invaders.last_left = [0, 0, 10]
        for coordinate in Invaders.coordinates:
            if coordinate:
                if Invaders.vel_x > 0:
                    if coordinate[2] >= Invaders.last_right[2]:
                        Invaders.last_right = coordinate
                elif Invaders.vel_x < 0:
                    if coordinate[2] <= Invaders.last_left[2]:
                        Invaders.last_left = coordinate
                coordinate[0] += Invaders.vel_x
                Invaders.all_invaders_are_dead = False
        if Invaders.all_invaders_are_dead:
           pass # game over
        Invaders.check_for_collision_with_walls()

    @staticmethod
    def create_bullets():
        if not Invaders.all_invaders_are_dead:
            if len(Invaders.bullets) < 4:
                bullet = random.choice(Invaders.invaders_that_can_shoot)
                if len(Invaders.bullets) >= 1:
                    # Prevents invaders bullets from being too close together and clumping together
                    if bullet[1] + 40 <= (Invaders.bullets[-1][1] - 30):
                        Invaders.bullets.append(bullet.copy())

                elif len(Invaders.bullets) < 1:
                    Invaders.bullets.append(bullet.copy())

    @staticmethod
    def shoot_bullets():
        for bullet in Invaders.bullets:
            pygame.draw.rect(win, red, (bullet[0] + 20, bullet[1] + 20, 5, 20))
            bullet[1] += 10
            if bullet[1] + 20 >= 650:
                Invaders.bullets.remove(bullet)

    @staticmethod
    def update_edge_invaders(invader_index):
        replace_invader = False
        for invader in Invaders.invaders_that_can_shoot:
            if invader is Invaders.coordinates[invader_index]:
                Invaders.invaders_that_can_shoot.remove(invader)
                replace_invader = True
                break
        Invaders.coordinates[invader_index] = None
        if not replace_invader:
            return      
        for i in range(4):
            if invader_index <= 10:
                break
            invader_index -= 11
            if Invaders.coordinates[invader_index]:
                Invaders.invaders_that_can_shoot.append(Invaders.coordinates[invader_index])
                break
            else:
                break

while run:
    pygame.time.delay(22)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.draw.rect(win, (120, 55, 220), (selection[0], selection[1], 270, 100), 2)
    win.fill((20, 20, 20))
    win.blit(text.render("LIVES: " + str(Player.lives), True, (0, 255, 0)), (930, 5))
    win.blit(text.render("SCORE: " + str(score), True, (0, 255, 0)), (5, 5))
    Invaders.create_invaders()
    Invaders.move_invaders()
    Player.refresh()
    Player.move()
    Invaders.create_bullets()
    Invaders.shoot_bullets()
    Player.create_bullets()
    Player.shoot()

    # Checks for collision between hero bullets and invaders  
    for i in range(len(Invaders.coordinates)):
        if not Invaders.coordinates[i]:
            continue
        for bullet in Player.bullets:
            if bullet[0] in range(Invaders.coordinates[i][0], Invaders.coordinates[i][0]+40):
                if bullet[1] in range(Invaders.coordinates[i][1], Invaders.coordinates[i][1]+40):
                    Invaders.update_edge_invaders(i)
                    Player.bullets.remove(bullet)
                    score += 1
                    break
                    
    
    # Checks for collision between invaders bullets and hero
    for shots in Invaders.bullets:
        if shots[0] + 5 in range(Player.head_x, Player.head_x+10):
            if shots[1] + 20 in range(Player.head_y, Player.head_y+10):
                Invaders.bullets.remove(shots)
                Player.lives -= 1
        elif shots[0] + 5 in range(Player.x, Player.x+40):
            if shots[1] + 20 in range(Player.y, Player.y+20):
                Invaders.bullets.remove(shots)
                Player.lives -= 1
        if Player.lives == 0:
            pass #game over

    pygame.display.update()

pygame.quit()
