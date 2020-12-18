#!/usr/local/bin/python3
#
# EuroMillones.py
#
# Alejandro Alvarez
#
# 18/12/2020

import random
import csv

def crear_solucion():
    solucion = []

    # Dos conjuntos de posibles numeros
    conjunto_1 = list(range(1,51))
    conjunto_2 = list(range(1,13))

    # Seleccionamos 5 del primer conjunto
    for i in range(5):
        index = random.randint(0, len(conjunto_1)-1)
        solucion.append(conjunto_1[index])
        # Eliminamos el elemento para evitar repetidos
        del conjunto_1[index]

    # Seleccionamos 2 del segundo conjunto
    for i in range(2):
        index = random.randint(0, len(conjunto_2)-1)
        solucion.append(conjunto_2[index])
        # Eliminamos el elemento para evitar repetidos
        del conjunto_2[index]

    return solucion

def es_valido(sol):
    solucion = sol.representation
    valido = True

    # El tamaño de la solucion es la primer verificacion que debemos hacer:
    if len(solucion) != 7:
        valido = False

    # Limite inferior
    if any(y < 1 for y in solucion):
        valido = False

    # Dividimos nuestra solucion en dos:
    cinco_numeros = solucion[0:5]
    estrellas = solucion[5:]

    # Limite superior
    if any(y > 50 for y in cinco_numeros):
        valido = False

    if any(y > 12 for y in estrellas):
        valido = False

    # Verificar repetidos
    repetidos = [x for x in cinco_numeros if cinco_numeros.count(x) > 1]
    repetidos += [x for x in estrellas if estrellas.count(x) > 1]

    if len(repetidos) > 0:
        valido = False

    return valido

class Fitness:
    def __init__(self,
               ruta = "euromillions.csv",
               sorteos = 104):
        self.historico = self.crear_historico(sorteos,ruta)

    def crear_historico(self, sorteos = 104, ruta = "euromillions.csv"):
        archivo = open(ruta, 'r')
        lector_csv = csv.reader(archivo, delimiter=';')
        datos_csv = list(lector_csv)
        del datos_csv[0:2]
        del datos_csv[sorteos:]
        estrellas = []
        pares = []
        numeros = []

        for linea in datos_csv:
            del linea[0]
            estrellas_linea = [linea[5],linea[6]]
            estrellas_linea.sort()
            estrellas.append(estrellas_linea)
            pares = pares + Fitness.pares_solucion(linea[:5])
            numeros = numeros + [int(x) for x in linea[:5]]
            linea = linea[:5]

        frecuencias = [0] * 51
        for numero in numeros:
            frecuencias[numero] = frecuencias[numero] + 1

        frecuencias_pares = [0] * 51
        for i in range(51):
            frecuencias_pares[i] = [0] * 51

        for par in pares:
            i = par[0]
            j = par[1]
            frecuencias_pares[i][j] = frecuencias_pares[i][j] + 1


        numeros.sort()
        return {'frecuencias':frecuencias,
                'frecuencias_pares':frecuencias_pares,
                'cinco_numeros': datos_csv}


    def evaluar_solucion(self, solucion):
        # Buscar todos los pares en la solución
        pares = Fitness.pares_solucion(solucion)
        probabilidad = 1
        for par in pares:
            probabilidad = probabilidad * self.calcular_probabilidad_par(par)

        probabilidad = probabilidad * self.probabilidad_repetir(solucion)

        return probabilidad


    def calcular_probabilidad_par(self, par):
        probabilidad = 1/2450
        cinco_numeros = self.historico["cinco_numeros"]
        frecuencias_pares = self.historico["frecuencias_pares"]
        frecuencias = self.historico["frecuencias"]

        if (frecuencias_pares[par[0]][par[1]] != 0):
            n1_n2 = frecuencias_pares[par[0]][par[1]]

            n1 = frecuencias[par[0]]
            n2 = frecuencias[par[1]]

            probabilidad = (n1_n2/(n1+n2))

        return probabilidad

    def probabilidad_repetir(self, solucion):
        repetir = 1
        if solucion in self.historico["cinco_numeros"]:
            repetir = 1/2118760
        return repetir

    def pares_solucion(solucion):
        pares = []
        for i in range(5):
            for j in range(i + 1, 5):
                par = [int(solucion[i]),int(solucion[j])]
                par.sort()
                pares.append(par)
        return pares
