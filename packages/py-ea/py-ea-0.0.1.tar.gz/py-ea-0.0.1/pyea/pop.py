import random


class Population():

    def __init__(self, generate_genotype=True, dimensions=50):
        self.dimensions = dimensions
        self.genotype = []

        self.fitness = 0

    def generate_genotype(self):
        self.genotype = [random.randint(-5, 5) for _ in range(self.dimensions)]

    def prettify_genotype(self):
        self.genotype = [round(self.genotype[i])
                         for i in range(self.dimensions)]

    def calculate_fitness(self):
        self.prettify_genotype()
        self.fitness = sum([abs(1-self.genotype[i]) if i % 2 == 0 else abs(0 -
                                                                           self.genotype[i]) for i in range(self.dimensions)])
