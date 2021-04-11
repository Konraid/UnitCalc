#!/usr/bin/env python3

import sys
import readline

from SIConverter import SIConverter
from term import TermParser
from ConstantsDict import ConstantsDict
import traceback

print('######################################')
print('#              UnitCalc              #')
print('######################################')
print('')
print('-> Add custom variables:')
print('     $ symbol    ;description    ;value[unit]')
print('     e.g.    $var    ;my variable    ;1[m]')
print('             $const  ;my constant    ;5')
print('')
print('-> Reuse last result:')
print('     "~"-symbol is placeholder for the last result')
print('     in the format of a valid input string')
print('')

#EXAMPLE
#
# >> c^2*G/5[m*s^2*Gy]
# Used c:  ['Vakuum-Lichtgeschwindigkeit', 299792458.0, 'm/s']
# Used G:  ['Gravitationskonstante', 6.6743e-11, '(m^3)*(kg^-1)*(s^-2)']
# ============================================
# 1.199712e+06 [s^(-4) * m^(2) * kg^(-1)]
# Better? Unit: [s^(-4) * m^(2) * kg^(-1)]

# >> $var;my variable;~
# Added temporary variable "var" :  ['my variable', 1199712.3378886282, 's^(-4) * m^(2) * kg^(-1)']

# >> 2*var^(-1)
# Used var:  ['my variable', 1199712.3378886282, 's^(-4) * m^(2) * kg^(-1)']
# ============================================
# 1.667066e-06 [s^(4) * m^(-2) * kg^(1)]
# Better? Unit: [s^(4) * m^(-2) * kg^(1)]

running = True
last_result = "1"

while running:
    try:
        input_string = str(input(">> ")).replace("~",last_result)
        if input_string == 'end' or input_string.startswith('exit'):
            running = False
            break
        elif input_string.startswith("$"):
            buffer = input_string[1::].split(";")
            ConstantsDict.getInstance().AddTempConstant(buffer[0],buffer[1],buffer[2])
        else:
            try:
                base_term = TermParser(input_string)
                print('============================================')
                print("{:e}".format(base_term.value), '[' + str(base_term.unit) + ']')
                last_result = str(base_term.value) + '[' + str(base_term.unit) + ']'
                print('Better? Unit: [' + SIConverter.getInstance().SIToUnit(base_term.unit.si_representation,
                                                                         10, 10) + ']')
            except KeyError:
                print("[ KeyError ] an unknown symbol occurred (probably), check input")
                traceback.print_exc()
    except EOFError:
        break
    print('')

print('')
print('ciao...')
