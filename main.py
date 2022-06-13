import pygame
import random

# COLOURS
BLACK = (0, 0, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0,0,255)
GOLD = (255, 215, 0)

# GAME PARAMS
game_width = 600
game_height = 600

sqr_width = 20
sqr_height = 20

pygame.init()
pygame.display.set_caption('Snake')

# SET TIMER
# snake movement
pygame.time.set_timer(pygame.USEREVENT, 100)
# apple spawn
pygame.time.set_timer(pygame.USEREVENT + 1, 2000)


class Window(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((game_width, game_height), 0, 32)
        self.direction = ''
        self.font1 = pygame.font.SysFont('Arial', 25)
        self.font2 = pygame.font.SysFont('Arial', 50)
        self.apples = []
        self.score = 0

    def addApple(self):
        rand_x = random.randint(0, 21)
        rand_y = random.randint(0, 21)
        apple = (rand_x, rand_y)
        self.apples.append(apple)

    def drawScreen(self):
        pygame.draw.rect(win.screen, GREEN,
                         (snake.positions[0][0] * 20, snake.positions[0][1] * 20, sqr_width, sqr_height), 0, 5)
        for pos in snake.positions[1::]:
            pygame.draw.rect(win.screen, CYAN, (pos[0] * 20, pos[1] * 20, sqr_width, sqr_height), 0, 5)
        for apple in self.apples:
            if apple in snake.positions:
                self.apples.remove(apple)
                self.score += 1
            else:
                pygame.draw.rect(win.screen, RED, (apple[0] * 20, apple[1] * 20, sqr_width, sqr_height), 0, 5)

        # score
        self.screen.blit(self.font1.render(f'Score: ', True, WHITE), (5, 10))
        self.screen.blit(self.font1.render(f'{self.score}', True, WHITE), (85, 10))

    def gameOver(self):

        # score
        self.screen.blit(self.font2.render('GAME OVER' if win.score < 900 else 'WELL DONE', True, RED if win.score < 900 else GOLD), (150, 250))
        self.screen.blit(self.font1.render(f'Score: {self.score}', True, RED if win.score < 900 else GOLD), (250, 320))

        #      restart button
        pygame.draw.rect(win.screen, RED if win.score < 900 else GOLD, (200, 375, 200, 50))
        self.screen.blit(self.font1.render(f'RESTART', True, WHITE), (245, 385))

    def checkRestart(self, x, y):
        if 200 <= x <= 400 and 375 <= y <= 425:
            return True
        else:
            return False

    def restart(self):
        self.apples = []
        self.score = 0
        self.direction = ''
        snake.__init__()


class Snake(object):
    def __init__(self):
        self.positions = [(15, 15)]


win = Window()
snake = Snake()


clock = pygame.time.Clock()

running = True
game_over = False

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if not game_over:
            if e.type == pygame.USEREVENT + 1:
                win.addApple()
            if e.type == pygame.USEREVENT:
                if win.direction == 'R':
                    snake.positions = [(snake.positions[0][0] + 1, snake.positions[0][1])] + snake.positions
                    snake.positions = snake.positions[0:win.score + 1]
                    # print(snake.positions)
                elif win.direction == 'L':
                    snake.positions = [(snake.positions[0][0] - 1, snake.positions[0][1])] + snake.positions
                    snake.positions = snake.positions[0:win.score + 1]
                    # print(snake.positions)
                elif win.direction == 'U':
                    snake.positions = [(snake.positions[0][0], snake.positions[0][1] - 1)] + snake.positions
                    snake.positions = snake.positions[0:win.score + 1]
                    # print(snake.positions)
                elif win.direction == 'D':
                    snake.positions = [(snake.positions[0][0], snake.positions[0][1] + 1)] + snake.positions
                    snake.positions = snake.positions[0:win.score + 1]
                    # print(snake.positions)

            if e.type == pygame.KEYDOWN:
                # right key
                if e.key == pygame.K_RIGHT:
                    if win.direction != 'L':
                        win.direction = 'R'

                    # left key
                elif e.key == pygame.K_LEFT:
                    if win.direction != 'R':
                        win.direction = 'L'

                    # UP key
                elif e.key == pygame.K_UP:
                    if win.direction != 'D':
                        win.direction = 'U'

                    # DOWN key
                elif e.key == pygame.K_DOWN:
                    if win.direction != 'U':
                        win.direction = 'D'
        elif game_over:
            if e.type == pygame.MOUSEBUTTONDOWN and win.checkRestart(pygame.mouse.get_pos()[0],
                                                                     pygame.mouse.get_pos()[1]):
                # print('Restart')
                game_over = False
                win.restart()

    for pos in snake.positions:
        if snake.positions.count(pos) > 1 or (pos[0] < 0 or pos[0] > 30 or pos[1] < 0 or pos[1] > 30):
            game_over = True

    win.screen.fill(BLACK)

    if not game_over:
        win.drawScreen()
    else:
        win.gameOver()

    pygame.display.flip()
    clock.tick(60)
    pygame.display.update()
