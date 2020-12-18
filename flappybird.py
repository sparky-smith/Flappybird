import pygame,sys,random

def draw_floor():  #defining function for the animation of the floors
    screen.blit(floor_surface,(floor_x_pos,680))
    screen.blit(floor_surface,(floor_x_pos+422,680))  #one behind another floor

def create_pipe():
    random_posy = random.choice(pipe_height) 
    bottom_pipe = pipe_surface.get_rect(midtop = (425,random_posy))
    top_pipe = pipe_surface.get_rect(midbottom = (425, random_posy - 300))
    
    return bottom_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
     
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 750:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe,pipe)
            

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            flap_hit.play()
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 680:
        return False
    return True
    

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,bird_movement * 3,1)
    return new_bird
        

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center= (100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (211,100))
        screen.blit(score_surface, score_rect)
    
    if game_state == 'game_over':
        high_score_surface = game_font.render(f"High Score: {int(high_score)}", True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (211,650))
        screen.blit(high_score_surface, high_score_rect)
        
        score_surface = game_font.render(f"Score: {int(score)}", True, (255,255,255))
        score_rect = score_surface.get_rect(center = (211,100))
        screen.blit(score_surface, score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    
    return high_score


pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512 )
#initializing pygame
pygame.init()


#drawing the screen
screen = pygame.display.set_mode((422, 750))
pygame.display.set_caption("Flappy Bird")
game_icon = pygame.image.load("flappysprites/iconflap.ico")
pygame.display.set_icon(game_icon)

#it decide the speed(frame per second) of the game
clock = pygame.time.Clock()

#font
game_font = pygame.font.Font('BigSpace-rPKx.ttf',40)

#Game variables
gravity = 0.2                   #the acceleration with which bird will go down
bird_movement = 0                #it will decide the up and down movement of the bird
game_active = True
score = 0
high_score = 0


#background
bg_surface = pygame.image.load('flappysprites/background-night1.png').convert()
#bg_surface = pygame.transform.scale2x(bg_surface)


#floor
floor_surface = pygame.image.load('flappysprites/base.png').convert()
#making a x cordinate variable
floor_x_pos = 0

#bird
bird_downflap = pygame.image.load('flappysprites/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('flappysprites/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('flappysprites/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index] 
bird_rect = bird_surface.get_rect(center = (100,375))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

#pipes
pipe_surface = pygame.image.load('flappysprites/pipe-green.png').convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [350,450, 550]

#game over surface
game_over_surface = pygame.image.load('flappysprites/gameover.png')
game_over_rect = game_over_surface.get_rect(center = (211,375))

#sound effects
flap_wing = pygame.mixer.Sound('Everything/sfx_wing.wav')
flap_hit = pygame.mixer.Sound('Everything/sfx_hit.wav')
flap_score = pygame.mixer.Sound('Everything/sfx_point.wav')
flap_score_countdown = 100


#Game loop
while True: 
 
    #checking the events
    for event in pygame.event.get():
        #quits the game with the clicking on the cross at right corner
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                #keeping the bird_movement to 0 as ther 
                #will not be much effect of gravity
                bird_movement = 0
                bird_movement -= 10   #going up with spacebar
                flap_wing.play()
                
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                bird_movement = 0
                bird_rect.center = (100,375)
                pipe_list.clear()
                score = 0
                
        
        
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            
        if event.type == BIRDFLAP: 
            if bird_index < 2:
                bird_index +=1
            else: 
                bird_index = 0
            
            bird_surface, bird_rect = bird_animation()
        
        
    #displaying background
    screen.blit(bg_surface,(0,0))

    if game_active:
        #making fall the bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        
        #displaying bird
        screen.blit(rotated_bird,bird_rect)
        
        game_active = check_collision(pipe_list) 
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score_display('main_game')
        score += 0.01
        flap_score_countdown -= 1
        if flap_score_countdown <= 0:
            flap_score.play()
            flap_score_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')
        
        
        
    #making run the floor to the left side
    floor_x_pos -= 1
    #calling the draw function to draw the floors
    draw_floor()
    
    #making the floor endless :)
    if floor_x_pos <= -422:
        floor_x_pos = 0
    
    


    pygame.display.update() # it updates the display of the game often and often
    clock.tick(120) #120 fps