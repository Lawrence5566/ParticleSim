#2 implement energy - make sure particles speed isnt random, its dependant on how much energy they have
#3 implement 2 different types of particles, make sure they are different colour etc
#4 implement reactions, particles need enough energy to react, if they do react, bonds are formed, this is exothermic
#so energy will need to be given off to the atmosphere?
#5 improve UI
#6 implement sliders, to change pressure, temperature, concentration(might make this a number you enter at the beggining)
#7 implement inputs and home screen etc
#8 implement the ability to react more than 2 types of particles
#9 fix init()problem

import math
import pygame
import random

pygame.init()

RED = 255,0,0
BLUE = 0,0,255
width, height = 1000, 600
backgroundColour = 255,255,255
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chemical Particles")

def addVectors(a,b):
    angle1 = a[0]       #pls no
    length1 = a[1]
    angle2 = b[0]
    length2 = b[1]
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2
    angle = 0.5 * math.pi - math.atan2(y, x)    #atan2 takes the x, y coords, works out the sign of the angle for us and work properly when x=0
    length = math.hypot(x, y)
    
    return (angle, length)

def collide(p1, p2):
    dx = p1.x - p2.x #difference in x cordinates
    dy = p1.y - p2.y
    
    dist = math.hypot(dx, dy)
    if dist < p1.radius + p2.radius:    #particles have collided!
        angle = 0.5 * math.pi + math.atan2(dy, dx)  #calculates current angle of the particle
        total_mass = p1.mass + p2.mass
        
        p1.angle, p1.speed = addVectors([p1.angle, p1.speed*(p1.mass-p2.mass)/total_mass], [angle, 2*p2.speed*p2.mass/total_mass])  #made these lists instead of tuples
        p2.angle, p2.speed = addVectors([p2.angle, p2.speed*(p2.mass-p1.mass)/total_mass], [angle+math.pi, 2*p1.speed*p1.mass/total_mass])

        overlap = 0.5*(p1.radius + p2.radius - dist+1)  #added upon testing and realising particles glitch into each other
        p1.x += math.sin(angle)*overlap
        p1.y -= math.cos(angle)*overlap
        p2.x -= math.sin(angle)*overlap
        p2.y += math.cos(angle)*overlap


class Particle():
    def _init_(self, mass, x, y, colour, speed, angle, radius): #none of this seems to work
        self.mass = 5  #different reacting particles need different masses
        self.x = 0
        self.y = 0
        self.colour = (255,255,255)
        self.speed = 0
        self.angle = 0
        self.radius = 10
        self.energy = 100

    def bounce(self):      #for bouncing off sides of screen
        if self.x > width - self.radius - 400:    #200 is for extra space to keep sliders at right side of screen 
            self.x = 2*(width - self.radius - 400) - self.x #particles will flash in -400 isnt in this line
            self.angle = - self.angle

        elif self.x < self.radius:
            self.x = 2*self.radius - self.x
            self.angle = - self.angle

        if self.y > height - self.radius:
            self.y = 2*(height - self.radius) - self.y
            self.angle = math.pi - self.angle

        elif self.y < self.radius:
            self.y = 2*self.radius - self.y
            self.angle = math.pi - self.angle
    
    #def convert(): #converts particles that sucesfully react to new particle
            
    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), 1, 0)
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.radius, 2)

    def move(self):
        #self.angle, self.speed = addVectors((self.angle, self.speed),gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y += math.cos(self.angle) * self.speed

no_particles = 20
allParticles = []

no_red = 0
for n in range(no_particles): #CREATING PARTICLES
    particle = Particle()
    
    particle.energy = 100
    particle.mass = 5  #different reacting particles need different masses
    particle.colour = (255,255,255)
    particle.radius = 10 
    particle.x = random.randint(particle.radius, particle.radius)
    particle.y = random.randint(particle.radius, particle.radius)
        
    if no_red > (no_particles/2 + 1): 
        particle.colour = BLUE
    else:
        particle.colour = RED
        no_red =+ 1
    particle.speed = particle.energy
    particle.angle = random.uniform(0, math.pi*2)
    allParticles.append(particle)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()   #get mosuse position
            #interface code for clicking buttons?

    screen.fill(backgroundColour)

    for i, particle in enumerate(allParticles):
        particle.move()
        particle.bounce()
        for particle2 in allParticles[i+1:]:
            collide(particle, particle2)
        particle.display()

    pygame.display.flip()
    pygame.display.update()























    
