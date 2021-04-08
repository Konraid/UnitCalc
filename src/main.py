#!/usr/bin/env python3

import sys

from SIConverter import SIConverter
from term import TermParser
from ConstantsDict import ConstantsDict

print('######################################')
print('#              UnitCalc              #')
print('######################################')
print('')
print('[ Syntax to add temporary constants:')
print('       $symbol; description; value; unit ]')
print('')

running = True

while running:
    input_string = str(input(">> "))
    if input_string == 'end':
        running = False
        break
    elif input_string.startswith("$"):
        ConstantsDict.getInstance().AddTempConstant(input_string[1::])
    else:
        base_term = TermParser(input_string)
        print('============================================')
        print("{:e}".format(base_term.value), '[' + str(base_term.unit) + ']')
        print('Better? Unit: [' + SIConverter.getInstance().SIToUnit(base_term.unit.si_representation,
                                                                     10, 10) + ']')

print('')
print('ciao...')
