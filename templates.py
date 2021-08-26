# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 21:19:32 2020

@author: Izabele
"""

class Cell:
    
    def __init__ (self, row, col, bombs):
        self.row = row
        self.col = col
        self.bombs = bombs
        self.rules = []
        self.guesses = []
        # something like this for rules [{2, ['a', 'b', 'c']}, {1, ['d', 'e']}]
        # something like this for guesses [{'a', 'b', 'c'}, {'a', 'c', 'd'}]
        
    def rebuild_rules_and_guesses (self):    
        pass
    
    def add_rule (self, rule):    
        self.rules.append(rule)
        
    def check_rules (self):
        """
        take action for rules that are definitive, i.e. either
        define where bombs or empty spaces are
        ex. {2, ['a', 'b']}, 2 bombs, 2 possible spaces
        ex. {0, ['c', 'd', 'e']}, 0 bombs, means all are empty spaces
        After updating bombs and empties globally, remove empty rules
        
        
        """
    
    

class MineSolver:
    """
    Examine the field in 4 stages/methods
    1. local ruleset
    2. global ruleset
        - used when there are no changes to local rulesets after one entire iteration over the field
    3. bomb ratio comparison
        - used when there are no changes to any rulesets after one entire iteration using the global ruleset
        - run simulations of how the rest of the field could appear, and then count the resulting final bombs
          keep running until there bomb # matches simulation #, if there are multiple feasible simulations, move on to next stage
    4. percentage (last resort)
        - used if 3 cannot be used yet, i.e. all cells are not yet contained in at least one ruleset
        - pick a space that has the highest chance to be empty and 'click' on it
        
    """
    
    self.bombs = []
    
    def __init__ (self, comparison, minefield):
        
        
        
class Compare:
    
    def __init__ (self):
        pass
    
    def rule_rule (self, rule1, rule2):     
        """
        If one rule list contains a rule that is a subset of another rule
        in the other rule list, copy that rule into the second list, and 
        have the rule list rebuilt by the cell
        """
        for r1 in rule1:
            for r2 in rule2:
                
                
    
    def guess_guess (self, guess1, guess2):
        pass
    
    def rule_guess (self, rule, guess):
        pass
    
    
        
        
    