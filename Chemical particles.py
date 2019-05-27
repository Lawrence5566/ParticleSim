import math
import pygame
import random

pygame.init()

arialFont = pygame.font.SysFont('Arial', 35, True)    #for title questions
arialFont2 = pygame.font.SysFont('Arial', 27, True)   #for buttons
freesansboldFont = pygame.font.Font('freesansbold.ttf', 50) #for no.particle input
textObj = pygame.font.Font('freesansbold.ttf', 25) #for sliders
BLACK = 0,0,0
YELLOW = (255,223,0) #golden yellow
SILVER = 193,197,201
RED = 255,0,0
BLUE = 0,0,255
PURPLE = 160,32,240
width, height = 1000, 600
backgroundColour = 255,255,255
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chemical Particles")

TemperatureModifier = 1 #slider changes this number  bounds  between 0.1 and 10 (bounds of sliderX need to scale to this)
PressureModifier = 1    
allParticles = []
e = 1    #if this number is 1, particles are 'perfect elastic particles'

def CalculateCollision(p1, p2, e):
    p1FinalVect = [0,0]
    p2FinalVect = [0,0]

    p2FinalVect[0] = ((p1.mass * p1.speedVect[0]) + (p2.mass * p2.speedVect[0]) + (p1.mass * (e * (p1.speedVect[0] - p2.speedVect[0])))) / (p1.mass + p2.mass) #x
    p2FinalVect[1] = ((p1.mass * p1.speedVect[1]) + (p2.mass * p2.speedVect[1]) + (p1.mass * (e * (p1.speedVect[1] - p2.speedVect[1])))) / (p1.mass + p2.mass) #y

    p1FinalVect[0] = p2FinalVect[0] - (e * (p1.speedVect[0] - p2.speedVect[0])) #x
    p1FinalVect[1] = p2FinalVect[1] - (e * (p1.speedVect[1] - p2.speedVect[1])) #y

    return p1FinalVect, p2FinalVect

def collide(p1, p2):
    dx = p1.x - p2.x #difference in x cordinates
    dy = p1.y - p2.y
    dist = math.hypot(dx, dy)
    tangent = math.atan2(dy, dx)    #tangent created between particles
    angle = 0.5 * math.pi + math.atan2(dy, dx)   #calculates current angle of the particle
    
    if dist < p1.radius + p2.radius:    #particles have collided!
        
        p1.speedVect,p2.speedVect = CalculateCollision(p1,p2,e)
        
        #particles get stuck in each other without this!
        angle = 0.5 * math.pi + tangent #calculates the angle between the two particles (which is 90 degrees to the tangent) and move the particles along this angle one pixel
        p1.x += math.sin(angle)     #stops particles from sticking together
        p1.y -= math.cos(angle)
        p2.x -= math.sin(angle)
        p2.y += math.cos(angle)



def react(p1, p2):
    dx = p1.x - p2.x #difference in x cordinates
    dy = p1.y - p2.y
    dist = math.hypot(dx, dy)
    
    if dist < p1.radius + p2.radius: 
        if p1.energy > activationEnergy and p2.energy > activationEnergy and p1.canReact == 1 and p2.canReact == 1:
            if p1.atomType != p2.atomType:      #makes sure hydrogen and hydrogen cant react together (for example)
                particle = Particle()

                bondEnergy = 0.464 #bond energy of H-O # temporaray while bond enthalpys are being made

                particle.energy = (p1.energy + p2.energy) - bondEnergy 
                
                particle.canReact = 0
                particle.mass = p1.mass + p2.mass
                particle.colour = (255,0,255)
                particle.radius = p1.radius + p2.radius
                particle.x = (p1.x + p2.x)/2 #mean adverage of both particle positions
                particle.y = (p1.y + p2.y)/2

                ##stops particle from spawing in the wall##
                if particle.x > width - particle.radius - 400: #Right      
                    particle.x -= particle.radius

                if particle.x < particle.radius + 25:  #Left
                    particle.x += particle.radius

                if particle.y > height - particle.radius -25: #Bottom
                    particle.y -= particle.radius

                if particle.y < particle.radius + 25:  #Top
                    particle.y += particle.radius

                p1speedvect,p2speedvect = CalculateCollision(p1,p2, 0)  #e is 0 so that particles come together, (uses tempoary variables), p1speedvect=p2speedvect
                
                particle.speedVect[0] =  p1speedvect[0]
                particle.speedVect[1] =  p1speedvect[1]

                allParticles.append(particle)

                p1.alive = 0
                p2.alive = 0
            else:
                return
        else:
            return
    else:
        return


class Particle():   
    def __init__(self):
        self.mass = 5  
        self.radius = 10
        self.energy = energyOfSystem/no_particles
        self.alive = 1
        self.speedVect = [0,0]

    def bounce(self):      #for bouncing off sides of screen
        if self.x >= width - self.radius - 400: #Right     #400 is for extra space to keep sliders at right side of screen 
            self.speedVect[0] = -self.speedVect[0]
            while self.x >= width - self.radius - 400:
                self.move()
      
        elif self.x <= self.radius + 25:  #Left
            self.speedVect[0] = -self.speedVect[0]
            while self.x <= self.radius + 25:
                self.move()

        if self.y >= height - self.radius -25: #Bottom
            self.speedVect[1] = -self.speedVect[1]
            while self.y >= height - self.radius -25:
                self.move()
            
        elif self.y <= self.radius + 25:  #Top
            self.speedVect[1] = -self.speedVect[1]
            while self.y <= self.radius + 25:
                self.move()

            
    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.radius, 2)

    def move(self):
        Xvelocity = self.speedVect[0] * TemperatureModifier * PressureModifier
        Yvelocity = self.speedVect[1] * TemperatureModifier * PressureModifier
        self.x += Xvelocity 
        self.y -= Yvelocity

        self.speed = math.sqrt((Xvelocity**2) + (Yvelocity**2))#works out the maginitude of the vector
        self.energy = 1/2*self.mass*(self.speed**2) #uses kinetic energy equation
        
def DisplayHome():
    homeScreen = [1,1]
    screen.fill(backgroundColour)

    #display "how many particles to simulate"#
    title = arialFont.render("How many particles to simulate? (press return to confirm) ", True, BLACK)
    titleRect = title.get_rect()
    titleRect.center = (475,100)

    #display "what would you like the activation energy to be?"#
    title2 = arialFont.render("how high do you want the activation energy to be?", True, BLACK)
    title2Rect = title2.get_rect()
    title2Rect.center = (475,340)

    #low,medium and high buttons for activation energy#
    lowButton = pygame.draw.rect(screen, BLACK,(225,400,100,50), 1) #X,Y,width,height
    lowButtonText = arialFont2.render("Low", True, BLUE)
    medButton = pygame.draw.rect(screen, BLACK,(425,400,100,50), 1)
    medButtonText = arialFont2.render("Medium", True, PURPLE)
    highButton = pygame.draw.rect(screen, BLACK,(625,400,100,50), 1)
    highButtonText = arialFont2.render("High", True, RED)

    TextValue = ""
    buttonClicked = ""
    numbers  = "0123456789"
    
    while homeScreen == [1,1] or homeScreen == [1,0] or homeScreen == [0,1]:
        pygame.key.get_pressed()

        #low,medium and high buttons for activation energy#
        if lowButton.collidepoint(pygame.mouse.get_pos()):                #nested if statements otherwise insideButton always ends up being "" dude to last else
            lowButton = pygame.draw.rect(screen, SILVER,(225,400,100,50), 1) #(surface, colour (X,Y,width,height), line thickness(0 is fill)
            insideButton = "low"
        else:
            lowButton = pygame.draw.rect(screen, BLACK,(225,400,100,50), 1)
            if medButton.collidepoint(pygame.mouse.get_pos()):
                medButton = pygame.draw.rect(screen, SILVER,(425,400,100,50), 1)
                insideButton = "med"
            else:
                medButton = pygame.draw.rect(screen, BLACK,(425,400,100,50), 1)
                if highButton.collidepoint(pygame.mouse.get_pos()):
                    highButton = pygame.draw.rect(screen, SILVER,(625,400,100,50), 1)
                    insideButton = "high"
                else:
                    highButton = pygame.draw.rect(screen, BLACK,(625,400,100,50), 1)
                    insideButton = ""

        if buttonClicked == "low":      #means the button stays looking 'clicked' without changing the inside button
            lowButton = pygame.draw.rect(screen, SILVER,(225,400,100,50), 1)
        if buttonClicked == "med":
            medButton = pygame.draw.rect(screen, SILVER,(425,400,100,50), 1)
        if buttonClicked == "high":
            highButton = pygame.draw.rect(screen, SILVER,(625,400,100,50), 1)
            
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:    #if keydown
                if pygame.key.name(event.key) in numbers:   #if they key pressed is in numbers list
                    screen.fill(backgroundColour)
                    TextValue += (pygame.key.name(event.key))   #add to Textvalue(string that get printed in the text box)
                elif pygame.key.name(event.key) == 'backspace':
                    screen.fill(backgroundColour)
                    TextValue = TextValue[:-1]      #remove the last value from the string
                elif pygame.key.name(event.key) == 'return' and len(TextValue) != 0:#if a number has been entered and enter is pressed particles are created
                    homeScreen[0] = 0
                if len(TextValue) > 2:      #stops number of particles being over 2 digits
                    TextValue = TextValue[:-1]
                    homeScreen[0] = 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if insideButton != "":
                    buttonClicked = insideButton #sets the button clicked to be the one the mouse is clicking
                    homeScreen[1] = 0
            if event.type == pygame.QUIT:
                pygame.quit()
    
                    
        Text = freesansboldFont.render(TextValue, True, BLACK)
        TextRect = Text.get_rect()
        TextRect.center = (490, 200)

        lowButton.center = (297,433)   #(+22,+8) on original centers so that text fits inside button boxes
        medButton.center = (477,433)    #(+2,+8)
        highButton.center = (696,433)  #(+21,+8)
        
        screen.blit(Text,TextRect)   
        screen.blit(title,titleRect)
        screen.blit(title2,title2Rect)
        screen.blit(lowButtonText,lowButton)
        screen.blit(medButtonText,medButton)
        screen.blit(highButtonText,highButton)
        pygame.display.flip()

    return TextValue,buttonClicked

### ###
no_particles,activationLevel = DisplayHome()
### ###

no_particles = int(no_particles)
energyOfSystem = no_particles*0.1 #gives particles an energy of 0.1 (MJ/mol)  #energyOfSingleParticle = energyOfSystem/no_particles = 0.1
print (activationLevel)
if activationLevel == "low":    #requires no increase in temp/pressure
    activationEnergy = (energyOfSystem/no_particles)*2.3 #takes energy of system / no. of particles to find each particles individual starting energy and sets it to x2.3
elif activationLevel == "med":  #requires a small increase in temp/pressure
    activationEnergy = (energyOfSystem/no_particles)*30  #sets it x30 
else: #(high)                   #requires a large increase in temp/pressure
    activationEnergy = (energyOfSystem/no_particles)*100  #sets it x100 #particles require a lot higher temp/pressure

FirstAtom = ("H",RED)   #contains atom type and colour 
no_FirstAtoms = int(no_particles/2)     #int the number to round it to the nearest whole integer
SecondAtom = ("O",BLUE)
no_SecondAtoms = (no_particles - no_FirstAtoms)

for n in range(no_particles): #CREATING PARTICLES
    particle = Particle()
    
    particle.canReact = 1  
    speed = ((2*particle.energy)/particle.mass)**0.5
    
    particle.speedVect[0] = random.choice([speed,-speed]) #picks between negative or positive direction
    particle.speedVect[1] = random.choice([speed,-speed])
    particle.x = random.randint(particle.radius + 25, width - particle.radius - 400)    #gives the particle a random x and y coord in the box
    particle.y = random.randint(particle.radius + 25, height - particle.radius - 25)

    if no_FirstAtoms != 0:
        particle.atomType = FirstAtom[0]
        particle.colour = FirstAtom[1]
        no_FirstAtoms -= 1
    else:
        particle.atomType = SecondAtom[0]
        particle.colour = SecondAtom[1]

    allParticles.append(particle)
    
clickingTempSlider = False

def DisplayGUI(TempSlider,TempSliderX,PressureSlider,PressureSliderX,clickingTemp,clickingPress):
    screen.fill(backgroundColour)

    ##Render Text for sliders##
    TempText = textObj.render("Temperature", True, BLACK)
    TempTextRect = TempText.get_rect()
    TempTextRect.center = (750, 270)
    screen.blit(TempText,TempTextRect)
    
    PressText = textObj.render("Pressure", True, BLACK)
    PressTextRect = PressText.get_rect()
    PressTextRect.center = (730, 425)
    screen.blit(PressText,PressTextRect)

    #borders of particle's box#
    pygame.draw.polygon(screen, BLACK, ((0,0),(25,0),(25,height),(0,height)), 0)   #right - top left point, top right, botton right, bottom left
    pygame.draw.polygon(screen, BLACK, ((0,0),(0,25),(width-400,25),(width-400,0)), 0) #top - top left,bottom left,bottom right,top right
    pygame.draw.polygon(screen, BLACK, ((0,height-25),(0,height),(width-400,height),(width-400,height-25))) #bottom - top left,bottom left, bottom right, top right
    pygame.draw.polygon(screen, BLACK, ((width-400,0),(width-400,height),(width-400+25,height),(width-400+25,0))) #bottom - top left,bottom left, bottom right, top right

    #slider rails#
    pygame.draw.line(screen, BLACK, (685,310),(950,310),3)
    pygame.draw.line(screen, BLACK, (685,460),(950,460),3)
    #slider center lines#
    pygame.draw.line(screen, BLACK,(817.5,295),(817.5,325),3)
    pygame.draw.line(screen, BLACK,(817.5,445),(817.5,475),3)
    
    if clickingTemp == True:  #if mouse is clicking Temperature Slider
        a = mouseX - 15         #center of slider
        if a >= 670 and a <= 935:   #boundaries of slider (x co-ordinates)
            TempSliderX = a
    TempSlider = pygame.draw.polygon(screen, YELLOW, [(TempSliderX,300),(TempSliderX,320),(TempSliderX+30,320),(TempSliderX+30,300)]) #top left,bottom left,bottom right,top right

    if clickingPress == True:  #if mouse is clicking pressure slider
        b = mouseX - 15         #center of slider
        if b >= 670 and b <= 935:   #boundaries of slider (x co-ordinates)
            PressureSliderX = b
    PressureSlider = pygame.draw.polygon(screen, YELLOW, [(PressureSliderX,450),(PressureSliderX,470),(PressureSliderX+30,470),(PressureSliderX+30,450)]) #top left,bottom left,bottom right,top right

    return TempSlider,TempSliderX,PressureSlider,PressureSliderX

TempSlider = pygame.draw.polygon(screen, YELLOW, [(800,300),(800,320),(830,320),(830,300)])
PressureSlider = pygame.draw.polygon(screen, YELLOW, [(800,450),(800,470),(830,470),(830,450)])
TempSliderX = 802.5     #TempSliderX should change the temperature, 802.5 is the 'middle' value, and ranges between 670 - 935
PressureSliderX = 802.5

clickingTemp,clickingPress = False,False

while True:
    TempSlider,TempSliderX, PressureSlider, PressureSliderX = DisplayGUI(TempSlider,TempSliderX,PressureSlider,PressureSliderX,clickingTemp,clickingPress)

    TemperatureModifier = math.exp((TempSliderX-800)/57)    #this equation will change if you change the slider range(X coordinates),
    PressureModifier = math.exp((PressureSliderX-800)/57)   #rearrangement of graph equation

    mouseX, mouseY = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and TempSlider.collidepoint(mouseX, mouseY):
            clickingTemp = True
            print("clickingTemp")
        elif event.type == pygame.MOUSEBUTTONDOWN and PressureSlider.collidepoint(mouseX, mouseY):
            clickingPress = True
            print("clickingPress")
        elif event.type == pygame.MOUSEBUTTONUP:
            clickingTemp, clickingPress = False,False
            
    for i,particle in enumerate(allParticles):
        if particle.alive == 1:
            particle.move()
            particle.bounce()
            for particle2 in allParticles[i+1:]:
                if particle2.alive == 1:
                    react(particle, particle2)      #needs to be first
                    collide(particle, particle2)
                else:
                    continue
            particle.display()
        else:
            continue

    pygame.display.flip()
    pygame.display.update()