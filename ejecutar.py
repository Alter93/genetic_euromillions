#!/usr/local/bin/python3
#
# ejecutar.py
#
# Alejandro Alvarez
#
# 17/12/2020

from algorithm.GeneticAlgorithm import GeneticAlgorithm
from algorithm.Solution import Solution
from algorithm.Operators import Operators
from algorithm.EuroMillones import crear_solucion, es_valido, Fitness

fitness = Fitness(sorteos = 104)
operators = Operators()

ga = GeneticAlgorithm(
                mutation = operators.euromillions_mutation,
                crossover = operators.euromillions_crossover,
                objective = fitness.evaluar_solucion,
                selection = operators.tournament_selection,
                initialization = crear_solucion,
                solution_size = 7,
                admissibility = es_valido,
                population_size = 50,
                generations = 150,
                crossover_p = .9,
                mutation_p = .2,
                elitism = True,
                )

population = ga.search_solutions()
print(f"{population[0].get_fitness()}")
