__author__  = "Helizonaldo Morais"
__version__ = "1.0.1"
__email__   = "helizonaldo@hotmail.com"

import time
import pygame, sys, random

x = 1024
y = 768
bg_color = (0,174,239)
white = (255,255,255)
norepeat = []
winner = 0
drawing = False

#load participants
participants = [line.strip() for line in open("participants.txt", 'r')]

pygame.init()
pygame.display.set_caption('_Sweepstakes_') 
pygame.time.set_timer(pygame.USEREVENT, 240)

screen = pygame.display.set_mode((1024, 768))
screen.fill(bg_color)

font = pygame.font.Font('Roboto-Black.ttf', 72) 

def text_objects(text, font):
    textSurface = font.render(text, True, white, bg_color)
    return textSurface, textSurface.get_rect()

def display_text_animation(name,phone):
    text = ''
    for i in range(len(name)):
        screen.fill(bg_color)
        text += name[i]
        text_surface, text_rect = text_objects(text, font)
        text_rect.center = ((x // 2),(y // 2))
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.wait(100)

    text_fone, text_rect_fone = text_objects(phone, font)
    text_rect_fone.center = ((x // 2),(y // 1.5))
    screen.blit(text_fone, text_rect_fone)
    pygame.display.update()


def drawingwinner(phone,name):
    def wrap(function):
        def wrapped(*args):      
            global winner
            if drawing:
                index = random.randint(0,len(participants)-1)
                if index not in norepeat:
                    screen.fill(bg_color)
                    function(participants[index].split(";")[0][-4:], participants[index].split(";")[1])
                    norepeat.append(index)    
                    winner = index                
            else:
                function(phone,name)

        return wrapped
    return wrap

@drawingwinner("* * * *","---")
def message_display(phone,name):
    print("display",phone,name)
    textPhone, TextRectP = text_objects(phone, font)
    TextRectP.center = ((x // 2),(y // 3))

    textName, TextRectN = text_objects(name, font)
    TextRectN.center = ((x // 2),(y // 2))

    screen.blit(textName, TextRectN)
    screen.blit(textPhone, TextRectP) 
    
message_display() 
running=True
while running:
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running=False

        if (event.type==pygame.KEYUP and not drawing):
            if event.key==pygame.K_RETURN:
                drawing = True
                start = 0
                winner = 0
                norepeat = []

        if drawing:
            #whether total participants less then 27, select 40% to show up else select 11
            count = round(len(participants)/2.5) if len(participants)<27 else 11
            if start < count:
                start += 1
                message_display()    
            else:
                drawing = False
                display_text_animation( participants[winner].split(";")[1], participants[winner].split(";")[0][-4:])
                participants.pop(winner) 
                
        pygame.display.update()

pygame.quit()
sys.exit()