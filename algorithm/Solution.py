#!/usr/local/bin/python3
#
# Solution.py
#
# Alejandro Alvarez
#
# 17/02/2020

from numpy.random import uniform,randint
from copy import deepcopy
import numpy as np
import pandas as pd
import math

class Solution:
    def __init__(self,
                 size,
                 objective,
                 initialization,
                 duplicate = False,
                 ):

        self.size = size
        self.representation = []

        self.calculate_objective = objective

        if duplicate == False:
            self.representation = initialization()



    def calculate_fitness(self):
        return self.calculate_objective(self.representation)

    def get_fitness(self):
        return self.calculate_objective(self.representation)



    def duplicate(self):
        new_solution = Solution(duplicate = True,
                                size = self.size,
                                objective = self.calculate_objective,
                                initialization = None )

        new_solution.representation = deepcopy(self.representation)



        return new_solution
