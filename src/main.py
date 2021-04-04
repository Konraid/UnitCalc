#!/usr/bin/env python3

import sys

from SIConverter import SIConverter
from term import TermParser

print('######################################')
print('#              UnitCalc              #')
print('######################################')
print('')

running = True

while running:
    input_string = str(input(">> "))
    if input_string == 'end':
        running = False
        break
    else:
        base_term = TermParser(input_string)
        print('============================================')
        print("{:e}".format(base_term.value), '[' + str(base_term.unit) + ']')
        print('Better? Unit: [' + str(SIConverter.getInstance().SIToUnit(base_term.unit.si_representation,
                                                                     10, 10)) + ']')

print('')
print('ciao...')
