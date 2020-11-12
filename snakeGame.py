import pygame 
import sys 
import random

#Game Setup
screen_width = 600
screen_height = 600

grid_size = 20
grid_width = screen_width/grid_size
grid_height = screen_height/grid_size

#Game Initialization
pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width,screen_height),0,32) #resolution, flags, bits used for color

pygame.display.set_caption("Saahil's snake game")

scoreList = []

#control directions
Up = (0,-1)
Down = (0,1)
Left = (-1,0)
Right = (1,0)

#represents the snake itself
class snake(object):
    def __init__(self):
        self.length = 1
        self.color = (80,118,249)
        self.position = [((screen_width/2),(screen_height/2))]
        self.dir = random.choice([Up,Down,Right,Left])
        self.score = 0

    def get_head_pos(self):
        return self.position[0]

    def turn(self, point):
        current = self.get_head_pos()
        if self.length > 1 and (point[0]*-1,point[1]*-1) == self.dir:
            Game_over(self.score) 
            self.reset()
            return
        else:
            self.dir = point 

    def move(self):
        curr_pos = self.get_head_pos()
        x,y = self.dir
        new = (((curr_pos[0] + (x * grid_size))%screen_width),((curr_pos[1] + (y * grid_size))%screen_height))

        if len(self.position) > 2 and new in self.position[2:]:
            Game_over(self.score) 
            self.reset()
        else:
            self.position.insert(0,new)
            if len(self.position) > self.length:
                self.position.pop()

    def reset(self):
        self.length = 1
        self.color = (80,118,249)
        self.position = [((screen_width/2),(screen_height/2))]
        self.dir = random.choice([Up,Down,Right,Left])
        self.score = 0
    
    def draw(self, surface):
        for pos in self.position:
            body_part = pygame.Rect((pos[0],pos[1]), (grid_size,grid_size))
            pygame.draw.rect(surface, self.color, body_part)
            pygame.draw.rect(surface,(44,44,44),body_part,1)
    
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.turn(Down)
                elif event.key == pygame.K_UP:
                    self.turn(Up)
                elif event.key == pygame.K_LEFT:
                    self.turn(Left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(Right)
          
#represents the food snake eats 
class food(object):
    def __init__(self):
        self.position = (0,0)
        self.color = (244,55,6)
        self.randomize_pos()

    def randomize_pos(self):
        self.position = (random.randint(1,grid_width-2)* grid_size, random.randint(1,grid_height-2)*grid_size)

    def draw(self,surface):
        pos = self.position
        food_particle = pygame.Rect((pos[0],pos[1]), (grid_size,grid_size))
        pygame.draw.rect(surface, self.color, food_particle)
        pygame.draw.rect(surface,(93, 216, 228),food_particle,1)

def draw_Grid(surface):
    borderColor = (192, 237, 114)
    for y in range(0,int(grid_height)):
        for x in range(0,int(grid_width)):
            if (x+y)%2 == 0:
                r1 = pygame.Rect((x*grid_size, y*grid_size),(grid_size,grid_size))
                if x*grid_size == 0 or x*grid_size == 580 or y*grid_size == 0 or y*grid_size == 580:
                     pygame.draw.rect(surface,borderColor,r1)
                else:
                    pygame.draw.rect(surface,(165,216,71),r1)
            else:
                r2 = pygame.Rect((x*grid_size, y*grid_size),(grid_size,grid_size))
                if x*grid_size == 0 or x*grid_size == 580 or y*grid_size == 0 or y*grid_size == 580:
                     pygame.draw.rect(surface,borderColor,r2)
                else:
                    pygame.draw.rect(surface,(142,204,57),r2)

def main():
    

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    draw_Grid(surface)

    snake1 = snake()
    food1 = food()

    myfont = pygame.font.SysFont("monospace",16)

    while True:
        clock.tick(10)
        #event handler
        snake1.handle_keys()
        draw_Grid(surface)
        snake1.move()
        if snake1.get_head_pos() == food1.position:
            snake1.length +=1
            snake1.score +=1
            food1.randomize_pos()
        curr = snake1.get_head_pos()
        
        if curr[0] == 0 and snake1.dir == Left:
          Game_over(snake1.score)  
          snake1.reset() 
        if curr[0] == 580 and snake1.dir == Right:
          Game_over(snake1.score) 
          snake1.reset() 
        if curr[1] == 0 and snake1.dir == Up:
          Game_over(snake1.score)   
          snake1.reset() 
        if curr[1] == 580 and snake1.dir == Down:
          Game_over(snake1.score)   
          snake1.reset() 

        snake1.draw(surface)
        food1.draw(surface)
        screen.blit(surface,(0,0))

        score_text = myfont.render("Score:{0}".format(snake1.score),2,(0,0,0))
        screen.blit(score_text, (5,2))

        pygame.display.update()

        

def main_menu():

    intro = True
     
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE:
                    intro = False

        screen.fill((192, 237, 114))
        menu_text = pygame.font.Font('freesansbold.ttf',50)
        small_menu_text = pygame.font.Font('freesansbold.ttf',20)
        textSurface = menu_text.render("Saahil's Snake Game", True, (0,0,0)) 
        introSurface = small_menu_text.render("Press space bar to play", True, (0,0,0))
        TextRect = textSurface.get_rect()
        SmallRect = introSurface.get_rect()
        TextRect.center = ((screen_width/2),(screen_height/2))
        SmallRect.center = ((screen_width/2),(screen_height/2+50))
        screen.blit(textSurface,TextRect)
        screen.blit(introSurface, SmallRect)
        pygame.display.update()
        clock.tick(15)

def Game_over(score):

    intro = True
    scoreList.append(score)
     
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE:
                    intro = False

        screen.fill((192, 237, 114))
        menu_text = pygame.font.Font('freesansbold.ttf',50)
        small_menu_text = pygame.font.Font('freesansbold.ttf',20)
        textSurface = menu_text.render("Score: {0}".format(score),2, (0,0,0)) 
        introSurface = small_menu_text.render("Press space bar to play again", True, (0,0,0))
        HscoreSurface = small_menu_text.render("High Score: {0}".format(max(scoreList)), 2, (0,0,0))
        TextRect = textSurface.get_rect()
        SmallRect = introSurface.get_rect()
        HSrect = HscoreSurface.get_rect()
        TextRect.center = ((screen_width/2),(screen_height/2))
        SmallRect.center = ((screen_width/2),(screen_height/2+50))
        HSrect.center = ((screen_width/2),(screen_height/2+100))
        screen.blit(textSurface,TextRect)
        screen.blit(introSurface, SmallRect)
        screen.blit(HscoreSurface, HSrect)
        pygame.display.update()
        clock.tick(15)
                
main_menu()
main()