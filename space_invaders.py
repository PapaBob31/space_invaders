
import pygame
import random
import copy
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
    def __init__(self, vel, lives):
        self.x = 500
        self.y = 550
        self.vel = vel
        self.lives = lives
        self.head_x = self.x + 15
        self.head_y = self.y - 10
        self.bullets = []

    def create_player(self):
        self.head_x = self.x + 15
        self.head_y = self.y - 10
        pygame.draw.rect(win, green, (self.x, self.y, 40, 10))
        pygame.draw.rect(win, green, (self.head_x, self.head_y, 10, 10))

    def move_player(self):
        keys = pygame.key.get_pressed()
        if self.x > 0:
            if keys[pygame.K_LEFT]:
                self.x -= self.vel
        if self.x + 40 < 1000:
            if keys[pygame.K_RIGHT]:
                self.x += self.vel

    def create_bullets(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bullet_pos = [self.head_x + 2, self.head_y - 5]
            if len(self.bullets) < 1:
                self.bullets.append(bullet_pos)
            elif len(self.bullets) >= 1:
                if self.head_y >= self.bullets[-1][1] + 100:
                    self.bullets.append(bullet_pos)

    def shoot(self):
        for bullet in self.bullets:
            pygame.draw.rect(win, green, (bullet[0], bullet[1], 5, 20))
            bullet[1] -= 10
            if bullet[1] <= 0:
                self.bullets.remove(bullet)

class Invaders:
    def __init__(self):
        self.vel_x = 5
        self.vel_y = 5
        self.width = 40
        self.height = 40
        self.bullet_pos = []
        self.bullets = []
        self.empty_columns = []
        self.no_of_columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        # Coordinates of all the invaders according to thir rows
        # the third item is a no (call it column-id) used to identify their columns which will be used later on in the code
        self.coordinates = [[[115, 20, 0], [185, 20, 1], [255, 20, 2], [325, 20, 3], [395, 20, 4], [465, 20, 5], [535, 20, 6], [605, 20, 7], [675, 20, 8], [745, 20, 9], [815, 20, 10]],
                            [[115, 80, 0], [185, 80, 1], [255, 80, 2], [325, 80, 3], [395, 80, 4], [465, 80, 5], [535, 80, 6], [605, 80, 7], [675, 80, 8], [745, 80, 9], [815, 80, 10]],
                            [[115, 140, 0], [185, 140, 1], [255, 140, 2], [325, 140, 3], [395, 140, 4], [465, 140, 5], [535, 140, 6], [605, 140, 7], [675, 140, 8], [745, 140, 9], [815, 140, 10]],
                            [[115, 200, 0], [185, 200, 1], [255, 200, 2], [325, 200, 3], [395, 200, 4], [465, 200, 5], [535, 200, 6], [605, 200, 7], [675, 200, 8], [745, 200, 9], [815, 200, 10]]]

    def create_invaders(self):
        for coordinate in self.coordinates:
            for pos in coordinate:
                pygame.draw.rect(win, red, (pos[0], pos[1], self.width, self.height))

    def move_invaders(self):
        def check_for_collision():
            index = 0
            first_invaders = []
            last_invaders = []
            move_down = False

            # Uses the length of the coordinates to append last and first items of each rows to different lists..
            # in a reversed order, starting from bottom to top
            for no in range(0, len(self.coordinates)):
                index -= 1
                first_invaders.append(self.coordinates[index][0])
                last_invaders.append(self.coordinates[index][-1])

            if self.vel_x > 0:
                # loops through the last item of each row to find the one that has reached the right edge of the window
                for invader in last_invaders:
                    if invader[0] + self.width >= 1000:
                        self.vel_x = -5
                        move_down = True
                        break
            elif self.vel_x < 0:
                # loops through the first item of each row to find the one that has reached the left edge of the window
                for invader in first_invaders:
                    if invader[0] <= 0:
                        self.vel_x = 5
                        move_down = True
                        break

            if move_down:
                for coordinate in self.coordinates:
                    # moves each invader horizontally after they collide with any of the edges of the window
                    for pos in coordinate:
                        pos[1] += self.vel_y

        if self.coordinates:
            for coordinate in self.coordinates:
                # moves each invader vertically
                for pos in coordinate:
                    pos[0] += self.vel_x
                if not coordinate:
                    # if all the invaders in a list has been killed, the list should be removed from coordinates
                    self.coordinates.remove(coordinate)
            check_for_collision()

    def check_position(self):
        """ Since the last row of the list are possible bullets position,
            python should search for other invaders with the same column-id as the dead ones
            from bottom to top and append them to the possible bullets pos (self.bullet_pos) to fill the gaps
        """
        empty_columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for number in list(range(11)):
            for position in self.coordinates[-1]:
                if number == position[2]:
                    empty_columns.remove(number)

        for no in empty_columns:
            for coordinate in reversed(self.coordinates):
                for pos in coordinate:
                    if pos[2] == no:
                        self.bullet_pos.append(pos.copy())
                        no = 13

    def create_bullets(self):
        if self.coordinates:
            # Uses the last row invaders positions as posible bullets position
            self.bullet_pos = copy.deepcopy(self.coordinates[-1])
            # If invaders still has more than one row
            if len(self.coordinates) > 1:
                if len(self.coordinates[-1]) < 11:
                    self.check_position()
                    print(self.bullet_pos[:5])
                    print(self.coordinates[-1][:5])
        
    def shoot_bullets(self):
        if self.coordinates:
            bullet = random.choice(self.bullet_pos)
            if len(self.bullets) < 4:
                if len(self.bullets) < 1:
                    self.bullets.append(bullet)
                if len(self.bullets) >= 1:
                    # Prevents invaders bullets from being too close together and clumping together
                    if bullet[1] + 40 <= (self.bullets[-1][1] - 30):
                        self.bullets.append(bullet)

            for bullet in self.bullets:
                pygame.draw.rect(win, red, (bullet[0] + 20, bullet[1] + 20, 5, 20))
                bullet[1] += 10
                if bullet[1] + 20 >= 650:
                    self.bullets.remove(bullet)


defender = Player(5, 3)
enemy = Invaders()
while run:
    pygame.time.delay(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.draw.rect(win, (120, 55, 220), (selection[0], selection[1], 270, 100), 2)
    win.fill((20, 20, 20))
    win.blit(text.render("LIVES: " + str(defender.lives), True, (0, 255, 0)), (930, 5))
    win.blit(text.render("SCORE: " + str(score), True, (0, 255, 0)), (5, 5))
    defender.create_bullets()
    defender.shoot()
    enemy.create_invaders()
    enemy.move_invaders()
    enemy.create_bullets()
    defender.create_player()
    defender.move_player()
    enemy.shoot_bullets()

    # Checks for collision between hero bullets and invaders  
    for pos_lists in enemy.coordinates:
        for invader in pos_lists:
            for bullet in defender.bullets:
                if bullet[0] in range(invader[0], invader[0]+40):
                    if bullet[1] in range(invader[1], invader[1]+40):
                        pos_lists.remove(invader)
                        defender.bullets.remove(bullet)
                        score += 1
    
    # Checks for collision between invaders bullets and hero
    for shots in enemy.bullets:
        if shots[0] + 5 in range(defender.head_x, defender.head_x+10):
            if shots[1] + 20 in range(defender.head_y, defender.head_y+10):
                enemy.bullets.remove(shots)
                defender.lives -= 1
        elif shots[0] + 5 in range(defender.x, defender.x+40):
            if shots[1] + 20 in range(defender.y, defender.y+20):
                enemy.bullets.remove(shots)
                defender.lives -= 1

    pygame.display.update()

pygame.quit()
