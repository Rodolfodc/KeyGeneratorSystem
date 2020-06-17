from math import sqrt
from fitness_functions import Fitness
from rabinM import generateSpace
import random


class Particle:
    def __init__(self, C1 = 2, C2 = 2, W = 0.5, F = 1):
        self.X = 0
        self.V = 0
        self.pBest = 0
        self.C1 = C1
        self.C2 = C2
        self.W = W
        self.F = F


    def update_X(self, ne):
            aux = self.X + self.V
            if (aux > ne-1) or (aux < 0) :
                self.X -= self.V
            else:
                self.X = aux
            self.X = int(self.X)

    def update_V(self, gBest, Vmax):
        self.V = self.F*(
                 self.W*self.V+
                 self.C1*random.random()*(self.pBest - self.X)+
                 self.C2*random.random()*(gBest.pBest - self.X)
                 )
        if self.V > Vmax:
            self.V = Vmax
        elif self.V < -Vmax :
            self.V = Vmax

    def verify_pBest(self, space):
        if space[self.X][4] > space[self.pBest][4]:
            #particle.pBest = particle.X
            return self.X
        else:
            return self.pBest

    def set_X(self, new_position):
        self.X = new_position

    def set_V(self, new_velocity):
        self.V = new_velocity

    def set_pBest(self, new_pBest):
        self.pBest = new_pBest

    def get_X(self):
        return self.X

    def get_V(self):
        return self.V

    def get_pBest(self):
        return self.pBest
        




#--------------------------------------------------------------------------------------------------------------------



class PSO:
    
    def __init__(self, np = 10, ne = 30, C1 = 2, C2 = 2, W = 0.5, Vmax = 15, iMax = 100, flag = False, fitness = [1], p = 0.8, space = None):
        self.np = np
        self.ne = ne
        self.C1 = C1
        self.C2 = C2
        self.W = W
        self.F = None
        self.Vmax = Vmax
        self.iMax = iMax
        self.flag = flag
        self.p = p
        self.space = space
        self.s = None
        self.fitness = Fitness(fitness,p)
        self.swarm = []
        self.gBest = 0

    def config_constriction(self):
        if self.flag:
            aux = self.C1 + self.C2
            self.F = 2/(abs(2 - aux - sqrt(aux**2 - 4*aux)))
        else:
            self.F = 1

    def swarm_initialization(self):
        if not self.swarm:
            for i in range(self.np):
                aux = Particle(self.C1, self.C2, self.W, self.F)
                self.swarm.append(aux)
                self.swarm[i].X = random.randint(0, (self.ne-1))
                self.swarm[i].pBest = self.swarm[i].X
                self.swarm[i].V = 0
            self.gBest = 0


    def evaluation(self, current_particle):
            tam = len(self.space[current_particle.X])
            if tam <= 4:
                evaluation_value = self.fitness.calculate(self.space[current_particle.X][3])# elemento = [p,q,e,k]
                self.space[current_particle.X].append(evaluation_value)

    def evaluate_all_particles(self):
        for i in range(self.np):
            self.evaluation(self.swarm[i])


    def execution(self):
        if self.space is None:
            self.space = generateSpace(self.ne, 1024)
        self.config_constriction()
        self.swarm_initialization()
        self.evaluate_all_particles()
        for j in range(self.iMax):
            for i in range(self.np):
                self.swarm[i].update_V(self.swarm[self.gBest], self.Vmax)
                self.swarm[i].update_X(self.ne)
                self.evaluation(self.swarm[i])
                self.swarm[i].pBest = self.swarm[i].verify_pBest(self.space)
            for i in range(self.np):
                if (self.space[self.swarm[i].pBest][4]) > (self.space[self.swarm[self.gBest].pBest][4]) :
                    self.gBest = i
            if self.space[self.swarm[self.gBest].pBest][4] == 1  or  self.space[self.swarm[self.gBest].pBest][4] >= self.p:
               
                break
        best_element = self.space[self.swarm[self.gBest].pBest]
        return best_element


    def set_swarm(self, new_swarm):
        self.swarm = new_swarm

    def set_space(self, new_space):
        self.space = new_space

    def set_gBest(self, new_gBest):
        self.gBest = new_gBest

    def get_swarm(self):
        return self.swarm

    def get_space(self):
        return self.space

    def get_gBest(self):
        return self.gBest

        
        


    
        
