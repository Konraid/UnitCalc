#!/usr/bin/env python3
from SIConverter import SIConverter
from term import TermParser

#input_string = str(input("Enter units: "))
input_string = '(2[kg]**4[kg]) / (2 [J^2/s*(N^2/(C))])'
input_string = '( ((((2 [J/C]^(2) ))) )/((2[m])^(1)))'
input_string = 'c'
base_term = TermParser(input_string)

print('============================================')
print("{:e}".format(base_term.value), '[' + str(base_term.unit) + ']')
print('Better? Unit: [' + str(SIConverter.getInstance().SIToUnit(base_term.unit.si_representation,
                                                            10, 10)) + ']')
