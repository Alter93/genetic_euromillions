#!/usr/local/bin/python3
#
# SingleObjective.py
#
# Alejandro Alvarez
#
# 21/02/2020

from .Solution import Solution
from .Operators import Operators
from numpy.random import uniform, randint
import math

class GeneticAlgorithm:
    def __init__(self,
                mutation,
                crossover,
                objective,
                selection,
                initialization,
                solution_size,
                admissibility,
                population_size = 100,
                generations = 200,
                crossover_p = .9,
                mutation_p = .2,
                elitism = True,
                ):

        # Initialization
        ###
        self.population_size = population_size
        self.generations = generations
        self.crossover_p = crossover_p
        self.mutation_p = mutation_p
        self.elitism = elitism
        self.objective = objective
        self.mutation_fn = mutation
        self.crossover_fn = crossover
        self.selection = selection
        self.is_admissible = admissibility

        # 1. Generate population of size N
        self.population = []
        for i in range(population_size):
            solution = Solution(size = solution_size,
                                objective = objective,
                                initialization = initialization
                                )
            self.population.append(solution)


    def search_solutions(self):
        for i in range(self.generations):
            print(f"Generation {i}: {self.population[0].get_fitness()}")
            children = []
            # Generate a new population
            while len(children) < self.population_size:
                (parent1, parent2) = self.selection(self.population)

                (child1, child2) = self.crossover(parent1, parent2)

                child1 = self.mutate(child1)
                child2 = self.mutate(child2)

                if self.is_admissible(child1):
                    children.append(child1)

                if self.is_admissible(child2):
                    children.append(child2)

            self.population = self.replace_population(children)

        return self.population


    def replace_population(self, population):
        new_population = population

        if self.elitism:
            total = self.sort_population(population + self.population)
            new_population = total[0:self.population_size]

        return new_population

    def sort_population(self, population):
        for i in range (0, len(population)):
            for j in range (i, len(population)):
                if (population[i].get_fitness() <
                    population[j].get_fitness()):

                    swap = population[j]
                    population[j] = population[i]
                    population[i] = swap

        return population

    def crossover(self, parent1, parent2):
        if uniform(0,1) < self.crossover_p:
            (child1,child2) = self.crossover_fn(parent1,parent2)
        else:
            child1 = parent1.duplicate()
            child2 = parent2.duplicate()

        return (child1,child2)

    def mutate(self, parent1):
        if uniform(0,1) < self.mutation_p:
            child = self.mutation_fn(parent1)
        else:
            child = parent1.duplicate()
        return child

    def select_nondominated(self):
        ## Actually selects unique solutions.
        ## Needs update
        last = (0,0)
        pareto_front = []
        for sol in self.population:
            if (sol.std_dev,sol.return_) != last:
                pareto_front = pareto_front + [sol]
                last = (sol.std_dev,sol.return_)
        return pareto_front
