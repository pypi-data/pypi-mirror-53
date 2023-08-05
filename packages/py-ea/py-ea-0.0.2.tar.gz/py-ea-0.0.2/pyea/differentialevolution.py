"""A Simple interface for Differential Evolution.

The Interface expects a Individual class with the following parameters and methods:

    parameters
    ------------------------------
    - genotype: a 1D list of values
    - fitness: a value scoring an individual
    - dimensions: the dimensions of the problem, i.e. the length of the genotype


    methods
    ------------------------------
    calculate_fitness(): a method to evaluate an individual
    generate_genotype(): a method to randomly instantiate the genotype of an individual
"""

from random import shuffle as _shuffle, randint as _randint, random as _random
from operator import lt
from matplotlib import pyplot as _plt
from functools import reduce as _reduce

__all__ = ["DifferentialEvolution", "search", "plot_history"]


def default_comparator(individual_1, individual_2):
    """
    individual_1: Individual class with

    """
    return individual_1.fitness < individual_2.fitness


class DifferentialEvolution():
    """Differential Evolution base class.

    Used to instantiate instances of differential evolution.

    Assumes the presence of an Individual class which is used to represent the population
    and evaluate individuals.
    """

    def __init__(self, Individual, comparator=default_comparator, population_size=20, generations=1000, number_of_mutagens=3, F=0.9, CR=0.5
                 ):
        """Initialize an instance.

        Individual: class representing population individuals.
            Assumes the following parameters:
            - genotype: a 1D list of values
            - fitness: a value scoring an individual
            - dimensions: the dimensions of the problem, i.e. the length of the genotype
            And the following functions:
            - calculate_fitness(): a method to evaluate an individual
            - generate_genotype(): a method to randomly instantiate the genotype of an individual
        comparator: function used to compare individuals
        number_of_mutagens:int , in [1,population_size)
        F: int, in (0,2]
        CR: int, in (0,1)

        """

        self.Individual = Individual
        self.comparator = comparator
        self.population_size = population_size
        self.generations = generations
        self.population = []
        self.number_of_mutagens = number_of_mutagens
        self.CR = CR
        self.F = F

        self.history = []

    def _valid_instance(self):
        return self.Individual and \
            self.population_size and \
            1 <= self.number_of_mutagens < self.population_size and \
            0 < self.F <= 2 and \
            0 < self.CR < 1

    def _validate_instance(self):
        if not self._valid_instance():
            raise RuntimeError(
                "The instance is not valid - some of the parameters are wrong")

    def _initialize_population(self):
        self.history = []  # Resetting history for subsequent runs
        self.population = [self._initialize_individual()
                           for _ in range(self.population_size)]

    def _initialize_individual(self):
        new_individual = self.Individual()
        new_individual.generate_genotype()
        new_individual.calculate_fitness()
        return new_individual

    def _get_best_individual(self):
        return _reduce(lambda individual_1, individual_2: individual_1 if self.comparator(individual_1, individual_2) else individual_2, self.population)

    def _select_mutagen_indices(self, target_index):
        mutagen_indices = []
        possible_mutagen_indices = [i for i in range(
            self.population_size) if i is not target_index]
        _shuffle(possible_mutagen_indices)
        mutagen_indices = possible_mutagen_indices[0:self.number_of_mutagens]
        return mutagen_indices

    def _calculate_mutagen_value(self, mutagen_indices, genotype_index):

        mutagen_values = [self.population[mutagen_index].genotype[genotype_index]
                          for mutagen_index in mutagen_indices]
        return sum([mutagen_values[0]]+[self.F*(mutagen_values[i]-mutagen_values[i+1])
                                        for i in range(1, self.number_of_mutagens-1)])

    def _generate_genotype_for_trial(self, target_index, dimensions, mutagen_indices):
        target = self.population[target_index]
        D = _randint(0, dimensions-1)
        return [self._calculate_mutagen_value(mutagen_indices, genotype_index) if _random(
        ) <= self.CR or genotype_index == D else target.genotype[genotype_index] for genotype_index in range(dimensions)]

    def _selection(self, trial, target):
        return trial if self.comparator(trial, target) else target

    def _crossover(self, target_index):
        mutagen_indices = self._select_mutagen_indices(target_index)
        trial = self._initialize_individual()
        trial.genotype = self._generate_genotype_for_trial(
            target_index, trial.dimensions, mutagen_indices)
        trial.calculate_fitness()
        return trial

    def _evolve_generation(self):
        next_generation = []
        for target_index in range(self.population_size):
            target = self.population[target_index]

            trial = self._crossover(target_index)
            next_generation.append(self._selection(trial, target))

        self.population = next_generation

    def _evolve_population(self):
        for _ in range(self.generations):
            self._evolve_generation()
            self.history.append(self._get_best_individual().fitness)

    def search(self):
        self._validate_instance()
        self._initialize_population()
        self._evolve_population()
        print("Best individual: ", self._get_best_individual().genotype)

    def plot_history(self):
        _plt.plot(self.history)
        _plt.show()
