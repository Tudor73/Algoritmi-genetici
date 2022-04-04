from copy import deepcopy
import math
from random import randint
from random import random
from chromosome import Chromosome

f = open("input.txt", 'r')

lista = [float(line.strip()) for line in f.readlines()]

n,a,b,coef1,coef2,coef3,p,pc,pm,etape = lista
n = int(n)
etape = int(etape)
coef1 = int(coef1)
coef2 = int(coef2)
coef3 = int(coef3)
p = int(p)
etape = int(etape)
pc = float(pc)
pm = float(pm)

l = int(math.log((b-a)*(10**p),2) + 1)

g = open('output.txt', 'w')
h = open('maxim.txt', 'w')

def generate_binary(l):
    return [randint(0,1) for i in range(l)]


def get_intervals(current_generation):
    intervals = [0]
    for chromosome in current_generation:
        intervals.append(intervals[-1] + chromosome.prob)
    return intervals

def binary_search(list, start, end, value):
    # if start > end:
    #     return start
    # m = (start + end) // 2
    # print(list[m])
    # if value < list[m]:
    #     binary_search(list, start, m-1, value)
    # elif value > list[m]:
    #     binary_search(list,m+1,end, value)
    # else:
        # return m
    while start <= end:
        m = (start + end) //2
        if value < list[m]:
            end = m - 1
        elif value > list[m]:
            start = m + 1
        else:
            return m
    return end 

def crossover(c1, c2):
    i = randint(0, l)
    g.write(f"{str(c1)} {str(c2)}, punct {i}\n")

    new_chromosome1 = c1[:i] + c2[i:]
    new_chromosome2 = c2[:i] + c1[i:]
    g.write(f"Rezultat {str(new_chromosome1)} {str(new_chromosome2)}\n")
    return new_chromosome1, new_chromosome2

def afisare_generatie(current_generation):
    for (i, chromosome) in enumerate(current_generation):
        g.write(f'{i}: {str(chromosome.value)} x = {chromosome.get_number(l,a,b)} f = {chromosome.get_function_value(coef1,coef2,coef3)}\n')

def afisare_selectie(current_generation):
    for (i,c) in enumerate(current_generation):
        g.write(f'cromozom {i} probabilitate: {c.prob}\n')

current_generation = [Chromosome(generate_binary(l)) for i in range(n)]



count = 0
while count < etape:
    max_value = 0
    total_sum = 0
    sum = 0
    elitist = None
    g.write(f"Generatia {count}\n")
    afisare_generatie(current_generation)

    for chromosome in current_generation:
        x = chromosome.get_number(l,a,b)
        f = chromosome.get_function_value(coef1, coef2, coef3)
        if f > max_value:
            max_value = f
        chromosome.function_value = f
        total_sum += f
    for chromosome in current_generation:
        chromosome.prob = chromosome.function_value / total_sum
        sum += chromosome.prob  
        if chromosome.function_value == max_value:
            elitist = chromosome
            
    afisare_selectie(current_generation)
    # current_generation.remove(elitist)
    intervals = get_intervals(current_generation)
    g.write("Intervale probabilitati selectie: \n")
    g.write(str(intervals)+ '\n')
    new_generation1 = []
    for i in range(n-1):
        u = random()
        x = binary_search(intervals, 0, len(intervals)-1, u)
        g.write(f'u = {u} selectam cromozomul {x}\n')
        new_generation1.append(deepcopy(current_generation[x]))
    
    g.write("Dupa selectie: \n\n")
    afisare_generatie(new_generation1)

    g.write(f"Probabilitatea de incrucisare: {pc}")
    chromosomes_to_crossover = []
    for (i,c) in enumerate(new_generation1):
        u = random()
        g.write(f'{i}: {str(c.value)}, u = {u}')
        if u < pc:
            g.write(f"< {pc} participa \n")
            chromosomes_to_crossover.append(i)
        else:
            g.write("\n")

    if len(chromosomes_to_crossover) % 2 == 1:
        chromosomes_to_crossover.pop()
    for i in range(0,len(chromosomes_to_crossover),2):
        g.write(f"Recombinare intre cromozomul {str(chromosomes_to_crossover[i])} cu {str(chromosomes_to_crossover[i+1])}\n")
        c1 = chromosomes_to_crossover[i]
        c2 = chromosomes_to_crossover[i+1]
        new_chromosome1, new_chromosome2 = crossover(new_generation1[c1].value, new_generation1[c2].value)
        new_generation1[c1].value = new_chromosome1
        new_generation1[c2].value = new_chromosome2
        new_generation1[c2].get_number(l,a,b)
        new_generation1[c2].get_function_value(coef1,coef2,coef3)

    g.write("Dupa recombinare: \n")
    afisare_generatie(new_generation1)

    for j,chromosome in enumerate(new_generation1):
        for i in range(len(chromosome.value)):
            u = random()
            if u < pm:  
                g.write(f"cromozomul {j} gena{i}\n")
                if chromosome.value[i] == 1:
                    chromosome.value[i] = 0
                elif chromosome.value[i] == 0:
                    chromosome.value[i] = 1
                chromosome.get_number(l,a,b)
                chromosome.get_function_value(coef1,coef2,coef3)

    g.write("Dupa mutatie: \n")
    afisare_generatie(new_generation1)

    current_generation = deepcopy(new_generation1)
    h.write(str(max_value)+"\n")
    count +=1
