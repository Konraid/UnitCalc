#!/usr/bin/env python3
import SIConverter
from term import TermParser

#input_string = str(input("Enter units: "))
input_string = '(2[kg]**4[kg]) / (3 [kg] + 7 [kg])'
input_string = '(2[kg]**4[kg]) / (3 + 7)'
base_term = TermParser(input_string)
base_term.evaluate()

print('============================================')
print(base_term.value, str('[' + str(base_term.unit) + ']'))
print('Better? Unit: ' + SIConverter.getInstance().SIToUnit(base_term.unit.si_representation))
