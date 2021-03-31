#!/usr/bin/env python3

from term import TermParser

#input_string = str(input("Enter units: "))
input_string = '(1[kg] + 20 [kg]) / (3 [kg] * 7 [kg])'
base_term = TermParser(input_string)
base_term.evaluate()

print('============================================')
print(base_term.value, str('[' + str(base_term.unit) + ']'))
