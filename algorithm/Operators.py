#!/usr/local/bin/python3
#
# Operators.py
#
# Alejandro Alvarez
#
# 18/02/2020

from numpy.random import randint, uniform
import numpy as np
import random

class Operators:
    def __init__(self,
                tournament_size = 10,
                ):
        self.mutation = self.euromillions_crossover
        self.selection = self.tournament_selection
        self.tournament_size = tournament_size

    def euromillions_crossover(self, parent1, parent2):
        parent_1 = parent1.representation
        parent_2 = parent2.representation
        numbers = parent_1[0:5] + parent_2[0:5]
        stars = parent_1[5:] + parent_2[5:]
        offspring_1 = []
        offspring_2 = []

        for i in numbers:
            if len(offspring_1) == 5:
                offspring_2.append(i)

            elif len(offspring_2) == 5:
                offspring_1.append(i)

            elif offspring_1.count(i) > 0:
                offspring_2.append(i)

            elif offspring_2.count(i) > 0:
                offspring_1.append(i)



            elif(random.uniform(0,1) > .5):
                offspring_1.append(i)

            else:
                offspring_2.append(i)


        for i in stars:
            if len(offspring_1) == 7:
                offspring_2.append(i)
            elif len(offspring_2) == 7:
                offspring_1.append(i)
            elif offspring_1[5:].count(i) > 0:
                offspring_2.append(i)
            elif offspring_2[5:].count(i) > 0:
                offspring_1.append(i)

            elif(random.uniform(0,1) > .5):
                offspring_1.append(i)
            else:
                offspring_2.append(i)

        child2 = parent1.duplicate()
        child1 = parent1.duplicate()

        child1.representation = offspring_1
        child2.representation = offspring_2

        return child1, child2

    def euromillions_mutation(self,sol):
        solution = sol.representation

        for _ in range(2):
            index = random.randint(0, 6)
            if index < 5:
                number = random.randint(1, 50)
                while(number in solution[0:5]):
                    number = random.randint(1, 50)
                solution[index] = number
            else:
                number = random.randint(1, 12)
                while(number in solution[5:]):
                    number = random.randint(1, 12)

                solution[index] = number

        new_sol = sol.duplicate()
        new_sol.representation = solution
        return new_sol

    def tournament_selection(self, population):
        indexes = []
        for i in range(0, self.tournament_size):
            selected_index = randint(0, len(population))

            indexes.append(selected_index)

        max_1 = -1000
        max_2 = -1000
        parent_1 = None
        parent_2 = None

        for i in indexes:
            fitness = population[i].calculate_fitness()
            if fitness > max_1:
                max_1 = fitness
                parent_1 = population[i]
            elif fitness >= max_2:
                max_2 = fitness
                parent_2 = population[i]

        return (parent_1, parent_2)
