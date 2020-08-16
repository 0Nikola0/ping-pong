import pygame
import os
import time


class Walls:
    def __init__(self, pos, size, color):
        self.pos = pos
        self.size = size
        self.color = color
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.pos, self.size))


class Paddles:
    def __init__(self, pos, size, color, vel):
        self.starting_pos = pos
        self.pos_x = int(pos[0])
        self.pos_y = int(pos[1])
        self.size = size
        self.color = color
        self.vel = vel

        self.rect = pygame.Rect(self.pos_x, self.pos_y, size[0], size[1])

    def update(self, pos_y):
        self.pos_y += pos_y
        self.rect.topleft = (self.pos_x, self.pos_y)

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.rect.topleft, self.size))


class Balls:
    def __init__(self, pos, size, color):
        self.pos = pos
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.size = size
        self.color = color
        self.dx = 1
        self.dy = 1

        self.dead = False
        self.points = 0

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.pos_x, self.pos_y), self.size)

    def update_ball_1p(self, leftp, rightp):
        self.pos_x += self.dx
        self.pos_y += self.dy
        # Ako udre goren dzid
        if self.pos_y > screenHeight - 20:
            self.pos_y -= 5
            self.dy *= -1
        # Dolen dzid
        elif self.pos_y < 25:
            self.pos_y += 5
            self.dy *= -1
        # Desen dzid, u ovaj slucaj paddle
        if self.pos_x >= rightp.pos_x:
            if rightp.rect.collidepoint((self.pos_x, self.pos_y)):
                self.pos_x -= 5
                self.dx *= -1
                self.points += 1
            else:
                # Ako ja promase paddle stavame deak e dead
                self.dead = True
        # Lev dzid ili player
        elif leftp.rect.collidepoint((self.pos_x, self.pos_y)):
            self.pos_x += 5
            self.dx *= -1

    def update_ball_2p(self, leftp, rightp):
        self.pos_x += self.dx
        self.pos_y += self.dy
        # Ako udre goren dzid
        if self.pos_y > screenHeight - 20:
            self.pos_y -= 5
            self.dy *= -1
        # Dolen dzid
        elif self.pos_y < 25:
            self.pos_y += 5
            self.dy *= -1
            # Desen dzid, u ovaj slucaj toa e paddle
        if self.pos_x >= rightp.pos_x:
            if rightp.rect.collidepoint((self.pos_x, self.pos_y)):
                self.pos_x -= 5
                self.dx *= -1
            else:
                # Ako ja promase paddle stavame deak e dead
                self.dead = True
        # Lev dzid ili player
        if self.pos_x <= leftp.pos_x:
            if leftp.rect.collidepoint((self.pos_x, self.pos_y)):
                self.pos_x += 5
                self.dx *= -1
            else:
                self.dead = True


####################################################
# x, y position where to show the window
windowPosition = (20, 43)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % windowPosition

screenWidth, screenHeight = 1000, 640
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GRAYB = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Pong')
font = pygame.font.Font(None, 50)
####################################################

paddleR = Paddles((screenWidth - 30, screenHeight / 2), (20, 100), BLACK, 2)
paddleL = Paddles((10, screenHeight / 2), (20, 100), BLACK, 2)
ball = Balls((100, 100), 10, WHITE)
walls_single = [Walls((screenWidth - 5, 0), (20, screenHeight), RED),
                Walls((0, 0), (20, screenHeight), GREEN),
                Walls((0, screenHeight - 20), (screenWidth, 20), GREEN),
                Walls((0, 0), (screenWidth, 20), GREEN)]
walls_twop = [Walls((screenWidth - 5, 0), (20, screenHeight), RED),
              Walls((-15, 0), (20, screenHeight), RED),
              Walls((0, screenHeight - 20), (screenWidth, 20), GREEN),
              Walls((0, 0), (screenWidth, 20), GREEN)]


def main_scene():
    single_player = font.render("1 Player", True, BLACK)
    single_rect = single_player.get_rect()
    single_rect.center = (int(screenWidth / 2), 305)
    two_player = font.render("2 Players", True, BLACK)
    two_rect = two_player.get_rect()
    two_rect.center = (int(screenWidth / 2), 345)
    main = True
    while main:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if single_rect.collidepoint(event.pos):
                    return False
                elif two_rect.collidepoint(event.pos):
                    return True

        screen.fill(GRAYB)
        screen.blit(single_player, single_rect)
        screen.blit(two_player, two_rect)
        pygame.display.flip()
    return False


def dead_scene():
    retry = font.render("Press R to try again", True, BLACK)
    retry_pos = retry.get_rect()
    retry_pos.center = (int(screenWidth / 2), int(screenHeight / 2))
    menu_btn = font.render("Main menu", True, BLACK)
    menu_btnpos = menu_btn.get_rect()
    menu_btnpos.topleft = (30, 30)
    dead = True
    while dead:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return running

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #   if menu_btnpos.collidepoint(event.type):
            #        main_menu = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            ball.dead = False
            ball.pos_x, ball.pos_y = 500, 320
            ball.dx *= -1
            ball.dy *= -1
            ball.points = 0
            running = True
            time.sleep(0.2)
            return running

        screen.fill(GRAYB)
        screen.blit(menu_btn, menu_btnpos)
        screen.blit(retry, retry_pos)
        pygame.display.flip()


def singleplayer():
    # NZ ovoa dali treba i so prae uopste
    # pygame.time.delay(5)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if ball.dead:
            running = dead_scene()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and paddleR.pos_y - 25 > paddleR.vel:
            paddleR.update(-paddleR.vel)
        if keys[pygame.K_DOWN] and paddleR.pos_y < screenHeight - paddleR.size[1] - 25:
            paddleR.update(paddleR.vel)

        screen.fill(GRAY)
        for wal in walls_single:
            wal.draw()
        paddleR.draw()
        ball.update_ball_1p(walls_single[1], paddleR)
        ball.draw()

        points = font.render(str(ball.points), True, BLACK)
        screen.blit(points, (50, 30))
        pygame.display.flip()


def twoplayers():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if ball.dead:
            running = dead_scene()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and paddleR.pos_y - 25 > paddleR.vel:
            paddleR.update(-paddleR.vel)
        if keys[pygame.K_DOWN] and paddleR.pos_y < screenHeight - paddleR.size[1] - 25:
            paddleR.update(paddleR.vel)

        if keys[pygame.K_w] and paddleL.pos_y - 25 > paddleL.vel:
            paddleL.update(-paddleL.vel)
        if keys[pygame.K_s] and paddleL.pos_y < screenHeight - paddleL.size[1] - 25:
            paddleL.update(paddleL.vel)

        screen.fill(GRAY)
        for wal in walls_twop:
            wal.draw()
        paddleR.draw()
        paddleL.draw()
        ball.update_ball_2p(paddleL, paddleR)
        ball.draw()
        pygame.display.flip()


if __name__ == "__main__":
    Players = main_scene()

    # True for 2 players, False for 1 player
    if Players:
        twoplayers()
    else:
        singleplayer()
