# Tilt v1.1 by Andy Crook 2016

# The aim of the game is to fill the screen as fast as possible by drawing with a pixel. Once full, the game will report
# a score to you called 'Delay', based on how long it took to win the game.
# Press a to reset back to a single pixel, abd B to start the game. B enables drawing mode and starts counting the delay





from microbit import *




# x,y coordinate for 'player'. These will be floating point values
x = 2
y = 2
old_x=-1
old_y=-1

clear_screen = 0 # a flag for if the player cursor draws permanantly to the screen or not
scoring=0 # a flag for if scoring is active or not
score=0 # the score for this game
easy=0  # a flag for easy mode 



def fade():
# a function to display a full block of colour and fade it in/out 5 times. This is diplayed as a winning condition
    display.clear()
    
    for t in range(0,5):
        # fade in
        for h in range(0,9):
            for f in range(0,5):
                for g in range(0,5):
                    display.set_pixel(f,g,h)
            sleep(30)
        # fade out    
        for h in range(0,9):
            for f in range(0,5):
                for g in range(0,5):
                    display.set_pixel(f,g,9-h)
            sleep(30)
            
    display.clear()



while True:

    x_reading = accelerometer.get_x()
    x=x+(x_reading/2000) # the /2000 determines how fast the player cursor moves depending on angle raised


    # check for out of bounds and reset it if that is the case
    if x<0:
        x=0
    if x>4:
        x=4
        
    # same again for y axis
    y_reading = accelerometer.get_y()
    y=y+(y_reading/2000)

    # check for y axis out of bounds and reset
    if y<0:
        y=0
    if y>4:
        y=4

    

    

    if button_b.is_pressed(): # game start button
        
        # only allow game to be started once, to properly record the easy mode a button
        if scoring == 0:
        
            if button_a.is_pressed():
                # if button a is pressed while the game starts, set the game as easy mode. This draws the screen
                # at a reduced color value, allowing the player to see thier own location
                easy = 1

            else:
                # easy mode off
                easy = 0

            # set the flag for clearing the screen to 1 - the game will not clear the screen. Stupid name for variable?
            # also, start scoring
            clear_screen = 1
            scoring=1

    
    # if the screen is to be cleared, clear it
    if clear_screen == 0:
        display.clear()
     
     
    # draw the player cursor - full brightness
    display.set_pixel(int(x),int(y),9)


    # easy mode, if == 1
    if easy == 1:
        
        # check if the current cursor is in a different place to where it was. If so, draw where it was with
        # less brightness
        if old_x != int(x) or old_y != int(y):
            if old_x!= -1:
                display.set_pixel(old_x,old_y,3)
        
            old_x=int(x)
            old_y=int(y)
        
    # end easy mode
    
    

    
    # if scoring is activated, add to the score every loop.
    if scoring ==1:
        score = score + 0.1

    
    # Check for winning condition. Only if all pixels have a value is the game won.
    won=1
    for f in range(0,5):
        for g in range(0,5):
            if display.get_pixel(f,g)==0:
                won=0

    
    # The game has been won
    if won ==1:
        score = int(score) # convert the score to an integer. It is the delay that the player took to solve the game
        # clear the display and fade the screen in and out - winning condition, then show a happy face
        display.clear()
        fade()
        display.show(Image.HAPPY)
        sleep(2000)

        
        # loop forever until reset
        while True:
            display.scroll("Delay: "+str(score))

