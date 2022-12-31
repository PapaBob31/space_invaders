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
        self.invaders_that_can_shoot = []
        self.bullets = []
        self.all_invaders_are_dead = False
        self.coordinates = [[115, 20, 0], [185, 20, 1], [255, 20, 2], [325, 20, 3], [395, 20, 4], [465, 20, 5], [535, 20, 6], [605, 20, 7], [675, 20, 8], [745, 20, 9], [815, 20, 10],
                            [115, 80, 0], [185, 80, 1], [255, 80, 2], [325, 80, 3], [395, 80, 4], [465, 80, 5], [535, 80, 6], [605, 80, 7], [675, 80, 8], [745, 80, 9], [815, 80, 10],
                            [115, 140, 0], [185, 140, 1], [255, 140, 2], [325, 140, 3], [395, 140, 4], [465, 140, 5], [535, 140, 6], [605, 140, 7], [675, 140, 8], [745, 140, 9], [815, 140, 10],
                            [115, 200, 0], [185, 200, 1], [255, 200, 2], [325, 200, 3], [395, 200, 4], [465, 200, 5], [535, 200, 6], [605, 200, 7], [675, 200, 8], [745, 200, 9], [815, 200, 10]]

        self.last_left =  self.coordinates[33]
        self.last_right = self.coordinates[-1]

        for i in range(33, 44):
            self.invaders_that_can_shoot.append(self.coordinates[i])

    def create_invaders(self):
        for coordinate in self.coordinates:
            if coordinate:
                pygame.draw.rect(win, red, (coordinate[0], coordinate[1], self.width, self.height))

    def check_for_collision_with_walls(self):
        move_invaders_down = False

        if self.vel_x > 0:
            if self.last_right[0] + self.width >= 1000:
                self.vel_x = -5
                move_invaders_down = True

        elif self.vel_x < 0:
            if self.last_left[0] <= 0:
                self.vel_x = 5
                move_invaders_down = True

        if move_invaders_down:
            for coordinate in self.coordinates:
                if coordinate:
                    coordinate[1] += self.vel_y

    def move_invaders(self):
        self.all_invaders_are_dead = True
        self.last_right = [0, 0, 0]
        self.last_left = [0, 0, 10]
        for coordinate in self.coordinates:
            if coordinate:
                if self.vel_x > 0:
                    if coordinate[2] >= self.last_right[2]:
                        self.last_right = coordinate
                elif self.vel_x < 0:
                    if coordinate[2] <= self.last_left[2]:
                        self.last_left = coordinate
                coordinate[0] += self.vel_x
                self.all_invaders_are_dead = False
        if self.all_invaders_are_dead:
            print('game over')
        self.check_for_collision_with_walls()

    def create_bullets(self):
        if not self.all_invaders_are_dead:
            if len(self.bullets) < 4:
                bullet = random.choice(self.invaders_that_can_shoot)
                if len(self.bullets) >= 1:
                    # Prevents invaders bullets from being too close together and clumping together
                    if bullet[1] + 40 <= (self.bullets[-1][1] - 30):
                        self.bullets.append(bullet.copy())

                elif len(self.bullets) < 1:
                    self.bullets.append(bullet.copy())

    def shoot_bullets(self):
        for bullet in self.bullets:
            pygame.draw.rect(win, red, (bullet[0] + 20, bullet[1] + 20, 5, 20))
            bullet[1] += 10
            if bullet[1] + 20 >= 650:
                self.bullets.remove(bullet)

    def update_edge_invaders(self, invader_index):
        replace_invader = False
        for invader in self.invaders_that_can_shoot:
            if invader is self.coordinates[invader_index]:
                self.invaders_that_can_shoot.remove(invader)
                replace_invader = True
                break
        self.coordinates[invader_index] = None
        if not replace_invader:
            return      
        for i in range(4):
            if invader_index > 10:
                invader_index -= 11
                if self.coordinates[invader_index]:
                    self.invaders_that_can_shoot.append(self.coordinates[invader_index])
                    break
            else:
                break

defender = Player(5, 3)
enemy = Invaders()
while run:
    pygame.time.delay(22)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.draw.rect(win, (120, 55, 220), (selection[0], selection[1], 270, 100), 2)
    win.fill((20, 20, 20))
    win.blit(text.render("LIVES: " + str(defender.lives), True, (0, 255, 0)), (930, 5))
    win.blit(text.render("SCORE: " + str(score), True, (0, 255, 0)), (5, 5))
    enemy.create_invaders()
    enemy.move_invaders()
    defender.create_player()
    defender.move_player()
    enemy.create_bullets()
    enemy.shoot_bullets()
    defender.create_bullets()
    defender.shoot()

    # Checks for collision between hero bullets and invaders  
    for i in range(len(enemy.coordinates)):
        if not enemy.coordinates[i]:
            continue
        for bullet in defender.bullets:
            if bullet[0] in range(enemy.coordinates[i][0], enemy.coordinates[i][0]+40):
                if bullet[1] in range(enemy.coordinates[i][1], enemy.coordinates[i][1]+40):
                    enemy.update_edge_invaders(i)
                    defender.bullets.remove(bullet)
                    score += 1
                    break
                    
    
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
