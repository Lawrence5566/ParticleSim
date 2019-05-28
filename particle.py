import math

class Particle():   
    def __init__(self, energyOfSystem, no_particles):
        self.mass = 5  
        self.radius = 10
        self.energy = energyOfSystem/no_particles
        self.alive = 1
        self.speedVect = [0,0]

    def bounce(self, width, height, TemperatureModifier, PressureModifier):      #for bouncing off sides of screen
        if self.x >= width - self.radius - 400: #Right     #400 is for extra space to keep sliders at right side of screen 
            self.speedVect[0] = -self.speedVect[0]
            while self.x >= width - self.radius - 400:
                self.move(TemperatureModifier, PressureModifier)
      
        elif self.x <= self.radius + 25:  #Left
            self.speedVect[0] = -self.speedVect[0]
            while self.x <= self.radius + 25:
                self.move(TemperatureModifier, PressureModifier)

        if self.y >= height - self.radius -25: #Bottom
            self.speedVect[1] = -self.speedVect[1]
            while self.y >= height - self.radius -25:
                self.move(TemperatureModifier, PressureModifier)
            
        elif self.y <= self.radius + 25:  #Top
            self.speedVect[1] = -self.speedVect[1]
            while self.y <= self.radius + 25:
                self.move(TemperatureModifier, PressureModifier)

            
    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.radius, 2)

    def move(self, TemperatureModifier, PressureModifier):
        Xvelocity = self.speedVect[0] * TemperatureModifier * PressureModifier
        Yvelocity = self.speedVect[1] * TemperatureModifier * PressureModifier
        self.x += Xvelocity 
        self.y -= Yvelocity

        self.speed = math.sqrt((Xvelocity**2) + (Yvelocity**2))#works out the maginitude of the vector
        self.energy = 1/2*self.mass*(self.speed**2) #uses kinetic energy equation
        
