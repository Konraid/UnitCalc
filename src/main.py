#!/usr/bin/env python3

from term import Term

input_string = input("Enter units: ")

base_term = Term(input_string)
base_term.evaluate()
