#!/usr/bin/env python3
from SIConverter import SIConverter
from term import TermParser

#input_string = str(input("Enter units: "))
input_string = '(2[kg]**4[kg]) / (3 [kg] + 7 [kg])'
input_string = '(2[kg]**4[kg]) / (2 [J^2/s*(N^2/(C))])'
base_term = TermParser(input_string)
base_term.evaluate()

print('============================================')
print(base_term.value, str('[' + str(base_term.unit) + ']'))
print('Better? Unit:' + str(SIConverter.getInstance().SIToUnit(base_term.unit.si_representation,
                                                            5, 5)))
