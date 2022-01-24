import pygame, sys, random
pygame.init()
screen = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()

class ParticlePrinciple:
    def __init__(self):
        self.particles = []
        self.movement = []

    def emit(self):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0][1] += particle[2][0]
                particle[0][0] += particle[2][1]
                particle[1] -= 0.1
                gravity = 4
                particle[0][1] += gravity
                if particle[0][1] > 500:
                    particle[0][1] -= 20
                if particle[0][0] > 500:
                    particle[0][0] -= 20
                if particle[0][0] < 0:
                    particle[0][0] += 20
                self.circle_rect = pygame.Rect(particle[0][0], particle[0][1],    particle[1], particle[1])
                pygame.draw.circle(screen,(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)), particle[0], int(particle[1]))
                

                #collisions
                if self.circle_rect.colliderect(Prect.rect):
                    particle[0][1] -= 20
                if self.circle_rect.right == Prect.rect.left:
                    particle[0][0] -= 20
                if self.circle_rect.left == Prect.rect.right:
                    particle[0][0] += 20
                if self.circle_rect.top == Prect.rect.bottom:
                    particle[0][1] += 40

                 

    def add_particles(self):
        pos_x = pygame.mouse.get_pos()[0]
        pos_y = pygame.mouse.get_pos()[1]
        radius = 15
        direction_x = random.randint(-3,3)
        direction_y = random.randint(-3,3)
        particle_circle =  [[pos_x,pos_y], radius,[direction_x, direction_y]]
        self.particle_circle1 =  [[pos_x,pos_y], radius,[direction_x, direction_y]]
        self.particles.append(particle_circle)


    def delete_particles(self):
        particle_copy = [particle for particle in self.particles if particle[1] > 0]
        self.particles = particle_copy


class ColliderRect:
    def __init__(self):
        rpx = 250
        rpy = 250
        width = 100
        height = 50
        self.rect = pygame.Rect(rpx, rpy,width, height)
    def draw_rect(self):
        pygame.draw.rect(screen, (196,0,196), self.rect)
        

        



Prect = ColliderRect()

PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT, 4)

particle1 = ParticlePrinciple()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == PARTICLE_EVENT:
            particle1.add_particles() 


    screen.fill((30,30,30))
    Prect.draw_rect()
    particle1.emit()
    pygame.display.update()
    clock.tick(120)
