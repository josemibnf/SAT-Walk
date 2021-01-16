#!/usr/bin/python3

import random
import sys
from api_pb2 import Interpretation

def parse(cnf):
    clauses = []
    count = 0
    n_vars = 0
    for clause in cnf.clause:
        c_list = []
        for literal in clause.literal:
            c_list.append(literal)
            if n_vars < abs(literal):
                n_vars = abs(literal)
        clauses.append(c_list)
        count += 1
    count = 0
    lit_clauses = [[] for _ in range(n_vars * 2 + 1)]
    for clause in clauses:
        for literal in clause:
            lit_clauses[literal + n_vars].append(count)
        count += 1
    return clauses, n_vars, lit_clauses

def get_random_interpretation(n_vars):
    return [i if random.random() < 0.5 else -i for i in range(n_vars + 1)]


def get_true_sat_lit(clauses, interpretation):
    true_sat_lit = [0 for _ in clauses]
    for index, clause in enumerate(clauses):
        for lit in clause:
            if interpretation[abs(lit)] == lit:
                true_sat_lit[index] += 1
    return true_sat_lit


def update_tsl(literal_to_flip, true_sat_lit, lit_clause):
    for clause_index in lit_clause[literal_to_flip]:
        true_sat_lit[clause_index] += 1
    for clause_index in lit_clause[-literal_to_flip]:
        true_sat_lit[clause_index] -= 1


def compute_broken(clause, true_sat_lit, lit_clause, omega=0.4):
    break_min = sys.maxsize
    best_literals = []
    for literal in clause:

        break_score = 0

        for clause_index in lit_clause[-literal]:
            if true_sat_lit[clause_index] == 1:
                break_score += 1

        if break_score < break_min:
            break_min = break_score
            best_literals = [literal]
        elif break_score == break_min:
            best_literals.append(literal)

    #Si el break_min esta en 0 significa que el literal escogido no hace ningun 'daño'.
    if break_min != 0 and random.random() < omega:
        best_literals = clause
        #Hay una probabilidad omega de que, si no hay un literal que nos perfecto, vayamos a barajar entre todos y no solo los de minimo 'daño'.

    return random.choice(best_literals)


def run_sat(clauses, n_vars, lit_clause, max_flips_proportion=4):
    max_flips = n_vars * max_flips_proportion
    while 1:
        interpretation = get_random_interpretation(n_vars)
        true_sat_lit = get_true_sat_lit(clauses, interpretation)
        for _ in range(max_flips):

            unsatisfied_clauses_index = [index for index, true_lit in enumerate(true_sat_lit) if
                                         not true_lit]

            if not unsatisfied_clauses_index:
                return interpretation

            clause_index = random.choice(unsatisfied_clauses_index)
            unsatisfied_clause = clauses[clause_index]

            lit_to_flip = compute_broken(unsatisfied_clause, true_sat_lit, lit_clause)

            update_tsl(lit_to_flip, true_sat_lit, lit_clause)

            interpretation[abs(lit_to_flip)] *= -1


def ok(cnf):
    clauses, n_vars, lit_clause = parse(cnf)
    solution = run_sat(clauses, n_vars, lit_clause)
    interpretation = Interpretation()
    interpretation.variable.extend(solution)
    return interpretation
