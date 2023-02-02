import pygame
import random

init_status = pygame.init()

#Timing setup  - this can be done better, but it isn't needed
#Time step represents miliseconds between frames
clock = pygame.time.Clock() 
time =0 
time_step = 100

#Game settings
#canvas of 1280x640 maintains the aspect ratio for our matrix of (2:1, 32x16). Each pixel is upscaled 40x.
fps = 60
canvas = width, height = 1280,640
pixel_size = 40
margin = 2 #creates a margin of 2 pixels around each rectangle to give a look and feel of a grid. set to 0 to turn off.


# Set display
pygame.display.set_caption("Snake Animator")
screen = pygame.display.set_mode(canvas)

##Snake settings
length = 1   #Starting length of snake
direction = (0,0) #wait for the player. dont move.
snake = pygame.rect.Rect([0,0,pixel_size-margin, pixel_size-margin]) #head of the snake
segments = [snake.copy()] #list of snake components. Ordered from tail to head. Made up of Rect objects that contains their coordinates

##food setup
food_pos = (320, 160) #this doesnt even do anything. It was inital food spawn.
food =pygame.Rect(food_pos[0], food_pos[1], pixel_size-margin, pixel_size-margin)
hungry = True #snake is hungry only after he consumes an apple. True lets the game know to spawn a new apple.

##Main game loop
while True:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            #quit game
            exit()
        
        """
        Controls for snake:
        *(WASD/arrow-keys)    movement
        *(spacebar/p)         pause game
        *(left-shift/h)       spawn apple in a new spot
        *(r)                  restart game
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                direction = (0,-pixel_size)
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                direction = (0,pixel_size)
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                direction = (-pixel_size,0)
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                direction = (pixel_size,0)
            if event.key ==pygame.K_p or event.key == pygame.K_SPACE:
                direction = (0,0)
            if event.key ==pygame.K_h or event.key == pygame.K_LSHIFT:
                hungry = True
            if event.key ==pygame.K_r:
                #for restarting
                direction = (0,0) 
                snake = pygame.rect.Rect([40,40,pixel_size-margin, pixel_size-margin])
                hungry = True
                food_pos = (320, 160)
                food =pygame.Rect(food_pos[0], food_pos[1], pixel_size-margin, pixel_size-margin)
                length = 2
                print("restarting")
                
    #Paint it black
    screen.fill("black")

    #Hunger system
    if hungry == True: #hungry when new food needs to spawn
        
        while True:
            #find spot outside of the snake body for an apple to spawn
            a = random.randrange(40, width-40, pixel_size)
            b = random.randrange(40, height-40, pixel_size)
            food_pos = [a,b]
            food = pygame.Rect(food_pos[0], food_pos[1], pixel_size-margin, pixel_size-margin)

            if pygame.Rect.collidelist(food, segments) == -1:
                break
                #returns -1 on no collision

        hungry = False
    

    # Drawfood
    pygame.draw.rect(screen, 'red', food)

    # colllison detection for if food is consumed 
    if pygame.Rect.colliderect(snake, food):
        hungry = True
        length +=1
        print(length)

    """
    # Very very frustrating collision detection for hitting you tail.
    # Optimially the goal is to collide with your tail, delete your snake head that is currently in another rectangle,
    # then use the last element in segements as your new head, but it never works or leaves gaps.
    # uncomment this to be experimental, otherwise you can collide with ur tail no biggies.
    """

    #if pygame.Rect.collidelist(snake, segments[:-1]) != -1:
        #snake =segments[-2]
        #pygame.draw.rect(screen, 'green', snake)
        #segments = segments[:-2]
        #direction =(0,0)
    

    # Move our snake
    time_now = pygame.time.get_ticks()
    if time_now - time > time_step:
        #framerate specific control. This is bad code, but it works.
        time = time_now
        if direction != (0,0):
            snake.move_ip(direction)      #move in-place the snake
            segments.append(snake.copy()) #add new snake segment with updated pos
            segments = segments[-length:]   #remove old pos before drawing.

            #snake is the independent rectangle we are moving
            #we copy the snake into the end of the segments list
            #removing the first item in the list, aka the tail position, so it appears that it is moving forward

    
    # Draw the snake
    for segment in segments:
        pygame.draw.rect(screen, 'green', segment)


    #update display            
    pygame.display.flip()
    clock.tick(fps)





