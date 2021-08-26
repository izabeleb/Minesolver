# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 01:47:53 2020

@author: Izabele
"""

    
from minefield import MineField
from cell import Cell
from utils import get_open_cells
   
    

def __main__():
#    ruleset1 = [[2, ['a', 'b', 'c', 'd']]]
#    ruleset2 = [[1, ['a', 'b']], [1, ['c']]]
#    
#    ruleset3 = 
#    
#    print("INITIAL RULESETS BEFORE CHANGE")
#    print("RS1: " + repr(ruleset1))
#    print("RS2: " + repr(ruleset2))
#    
#    ruleset1, ruleset2 = compare_2_rulesets(ruleset1, ruleset2)
#                
#    print("RULESETS AFTER COMPARISON")
#    print("RS1: " + repr(ruleset1))
#    print("RS2: " + repr(ruleset2))
#    
#    print("PRUNED RULESET1")
#    print(prune_ruleset(ruleset1))
    
#    ruleset1 = [[1, ['a', 'b', 'c']]]
#    ruleset2 = [[1, ['g', 'f', 'e']]]
#    guesses = [
#            ['b', 'c', 'd'],
#            ['b', 'c', 'e'],
#            ['b', 'c', 'f'],
#            ['c', 'd', 'e'],
#            ['c', 'd', 'f'],
#            ['b', 'd', 'e'],
#            ['b', 'e', 'f'],
#            ['c', 'e', 'f'],
#            ['d', 'e', 'f'],
#            ['b', 'd', 'f']
#            ]
#    
#    new_guesses1 = compare_ruleset_and_guesses(ruleset1, guesses)
#    new_guesses2 = compare_ruleset_and_guesses(ruleset2, new_guesses1)
#    print(new_guesses2)

    field = MineField(4, 4, None, 1)
    print(field)
    
    first_click_row = int(field.max_row / 2)
    first_click_col = int(field.max_col / 2)
    
    cell = field.get_cell_at(first_click_row, first_click_col)
    
    if cell.is_mine:
        new_loc: tuple = field.move_mine(cell)
        old_loc: tuple = (cell.row, cell.col)
        
    print("Cell row: " + str(cell.row) + " cell col: " + str(cell.col))
    open_cells: list = get_open_cells(field, cell)
    open_set = set(open_cells)
    print(repr(open_cells))
    print(repr(open_set))
     thing = 5
    

def rs_contains_rule (ruleset, rule):
    for r in ruleset:
        if r == rule:
            return True
        
    return False

def compare_2_rulesets (ruleset1, ruleset2):
    # potentially remove one of 2 if statements, since
    # you're looping over both rulesets, each combination must be reached
    # eventually
    for r1 in ruleset1:
        for r2 in ruleset2:
            if set(r1[1]).issubset(set(r2[1])):
                if not rs_contains_rule(ruleset2, r1):
                    ruleset2.append(r1)
                
            if set(r2[1]).issubset(set(r1[1])):
                if not rs_contains_rule(ruleset1, r2):
                    ruleset1.append(r2)
                    
    return ruleset1, ruleset2

def compare_ruleset_and_guesses (ruleset, guesses):
    valid_guesses = []
    
    for rule in ruleset:
        rule_dict = {}
        for cell_id in rule[1]:
            if cell_id in rule_dict:
                rule_dict[cell_id] += 1
            else:
                rule_dict[cell_id] = 1
        for guess in guesses:
            guess_dict = rule_dict.copy()
            for guess_single_cell_id in guess:
                if guess_single_cell_id in guess_dict:
                    guess_dict[guess_single_cell_id] += 1
                else:
                    guess_dict[guess_single_cell_id] = 1
                    
            num_similarities = sum(map((2).__eq__, guess_dict.values()))
            if num_similarities <= rule[0]:
                valid_guesses.append(guess)
    return valid_guesses

def prune_guesses (guesses):
    num_guesses = len(guesses)
    guess_dict = {}
    for guess in guesses:
        for guess_single_cell_id in guess:
            if guess_single_cell_id in guess_dict:
                guess_dict[guess_single_cell_id] += 1
            else:
                guess_dict[guess_single_cell_id] = 1

    for k, v in guess_dict.iteritems():
        if v == num_guesses:
            # TODO: append to rules for that cell
            # this.rules.append([1, [k]])
            pass
    
def prune_ruleset (ruleset):
    for r1 in ruleset:
        for r2 in ruleset:
            if (r1 != r2) and (r1[0] != 0) and (r2[0] != 0):
                if set(r1[1]).issubset(set(r2[1])):
                    r2[0] = r2[0] - r1[0]
                    r2[1] = [x for x in r2[1] if x not in r1[1]]
                    ruleset_no_duplicates = []
                    [ruleset_no_duplicates.append(x) for x in ruleset if x not in ruleset_no_duplicates]
    return ruleset_no_duplicates

def check_rules (ruleset):
    for rule in ruleset:
        # all cells in this rule are empties
        if rule[0] == 0:
            # TODO: perform click on all empty cells
            #
            #
            # and then remove them
            ruleset.remove(rule)
        # all cells in this rule are bombs
        elif rule[0] == len(rule[1]):
            # update global bomb list and counter,
            # and also maybe update global ruleset
            pass

__main__()
    