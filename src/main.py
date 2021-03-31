#!/usr/bin/env python3
from SIConverter import SIConverter
from term import TermParser

#input_string = str(input("Enter units: "))
input_string = '(2[kg]**4[kg]) / (2 [J^2/s*(N^2/(C))])'
input_string = '(2^13)/(3^8) * ( (1.097[1/m]*10^7)^3 * 5[m/s]*2[m^2])/(1)'
base_term = TermParser(input_string)

print('============================================')
print("{:e}".format(base_term.value), str('[' + str(base_term.unit) + ']'))
print('Better? Unit:' + str(SIConverter.getInstance().SIToUnit(base_term.unit.si_representation,
                                                            10, 10)))
