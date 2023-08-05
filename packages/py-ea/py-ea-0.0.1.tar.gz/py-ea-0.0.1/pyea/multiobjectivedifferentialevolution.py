from random import shuffle as _shuffle, randint as _randint, random as _random
from operator import lt
from matplotlib import pyplot as _plt
from functools import reduce as _reduce


class MultiObjectiveDifferentialEvolution():

    def __init__(self, Individual, population_size=50, generations=1000, number_of_mutagens=3, F=0.9, CR=0.5):

        self.Individual = Individual
        self.population_size = population_size
        self.generations = generations
        self.number_of_mutagens = number_of_mutagens
        self.F = F
        self.CR = CR

        self.population = []

    def _is_valid_instance(self):
        return self.Individual and \
            self.population_size and \
            1 <= self.number_of_mutagens < self.population_size and \
            0 < self.F <= 2 and \
            0 < self.CR < 1

    def _validate_instance(self):
        if not self._is_valid_instance():
            raise RuntimeError(
                "The instance is not valid - some of the parameters are wrong")

    def _initialize_individual(self):
        new_individual = self.Individual()
        new_individual.generate_genotype()
        new_individual.calculate_fitness()
        return new_individual

    def _initialize_population(self):
        self.population = [self._initialize_individual()
                           for _ in range(self.population_size)]

    def _select_mutagen_indices(self, target_index):
        possible_indices = [
            i for i in range(self.population_size) if i is not target_index]
        _shuffle(possible_indices)
        mutagen_indices = possible_indices[:self.number_of_mutagens]
        return mutagen_indices

    def _calculate_mutagen_value(self, mutagen_indices, genotype_index):
        mutagen_values = [self.population[mutagen_index].genotype[genotype_index]
                          for mutagen_index in mutagen_indices]
        return mutagen_values[0] + [self.F * (mutagen_values[i]-mutagen_values[i+1])
                                    for i in range(1, self.number_of_mutagens-1)]

    def _generate_genotype_for_trial(self, target_index, mutagen_indices, dimensions):
        target = self.population[target_index]
        D = _randint(0, dimensions-1)
        return [self._calculate_mutagen_value(mutagen_indices, genotype_index) if _random() < self.CR or genotype_index == D else target.genotype[genotype_index] for genotype_index in range(dimensions)]

    def _crossover(self, target_index):
        trial = self.Individual()
        mutagen_indices = self._select_mutagen_indices(target_index)
        trial.genotype = self._generate_genotype_for_trial(
            target_index, mutagen_indices, trial.dimensions)
        return trial

    def _evolve_generation(self):
        for target_index in range(self.population_size):
            target = self.population[target_index]
            trial = self._crossover(target_index)
            trial.calculate_fitness()
            if trial.dominates(target):
                self.population[target_index] = trial
            elif not target.dominates(trial):
                self.population.append(trial)
        # TODO: implement pruning using non-dominating sort and crowding distance

    def _evolve_population(self):
        for _ in range(self.generations):
            self._evolve_generation()
        return

    def search(self):
        self._initialize_population()
        self._evolve_population()
