from unit import Unit
import math

class TermParser:
    def getIndexOutOfBrackets(self, symbol, string):
        bracket_counter = 0
        for i in range(0, len(string)):
            s = string[i]
            if s == '(':
                bracket_counter += 1
            elif s == ')':
                bracket_counter -= 1
            if s == symbol and bracket_counter == 0:
                return i
        return -1

    def checkNumOfBrackets(self, string):
        bracket_counter = 0
        for i in range(0, len(string)):
            s = string[i]
            if s == '(':
                bracket_counter += 1
            elif s == ')':
                bracket_counter -= 1
        return bracket_counter == 0

    def __init__(self, term_text):
        term_text = term_text.replace(' ', '')

        # region definition of members
        self.unit = None
        self.value = None
        self.term_text = None
        # endregion

        # check for correct use of parentheses
        if not self.checkNumOfBrackets(term_text):
            print('[ERROR] Opening Brackets are not matching closing ones')
            return

        # region remove redundant parentheses
        bracket_counter = 1
        remove_brackets = False
        if term_text.startswith('(') and term_text.endswith(')'):
            remove_brackets = True
            for i in range(1, len(term_text)):
                s = term_text[i]
                if s == '(':
                    bracket_counter += 1
                elif s == ')':
                    bracket_counter -= 1
                if bracket_counter <= 0 and i <len(term_text) -1:
                    remove_brackets = False
                    break
        if(remove_brackets):
            term_text = term_text[1:-1]
        # endregion

        term_text = term_text.replace('**', '^')
        self.term_text = term_text

        index = self.getIndexOutOfBrackets('+', term_text)
        if index != -1:
            self.operator = "+"
            self.term_a = TermParser(term_text[0:index])
            self.term_b = TermParser(term_text[index + 1::])
            return

        index = self.getIndexOutOfBrackets('-', term_text)
        if index != -1:

            self.operator = "-"
            self.term_a = TermParser(term_text[0:index])
            self.term_b = TermParser(term_text[index + 1::])
            return

        index = self.getIndexOutOfBrackets('^', term_text)
        if index != -1:
            self.operator = "^"
            self.term_a = TermParser(term_text[0:index])
            self.term_b = TermParser(term_text[index + 1::])
            return

        index = self.getIndexOutOfBrackets('*', term_text)
        if index != -1:
            self.operator = "*"
            self.term_a = TermParser(term_text[0:index])
            self.term_b = TermParser(term_text[index + 1::])
            return

        index = self.getIndexOutOfBrackets('/', term_text)
        if index != -1:
            self.operator = "/"
            self.term_a = TermParser(term_text[0:index])
            self.term_b = TermParser(term_text[index + 1::])
            return

    def evaluate(self):
        if not hasattr(self, 'operator'):
            # at this point there should be something like 2[N/m]
            if '[' in self.term_text:
                self.value = float(self.term_text[:self.term_text.find('[')])
                self.unit = Unit.with_string(self.term_text[self.term_text.find('[') + 1::-1], True)
            else:
                self.value = float(self.term_text)
                self.unit = Unit.identity()
            return self
        else:
            self.term_a.evaluate()
            self.term_b.evaluate()
            if self.operator == '+' or self.operator == '-':
                if self.term_a.unit == self.term_b.unit:
                    if self.operator == "+":
                        self.value = self.term_a.value + self.term_b.value
                    else:
                        self.value = self.term_a.value - self.term_b.value
                    self.unit = self.term_a.unit
                    return self
                else:
                    print('[ERROR] Units do not match in sum.')
                    print('>>', self.term_text)
            elif self.operator == '*':
                self.value = self.term_a.value * self.term_b.value
                self.unit = self.term_a.unit * self.term_b.unit
                return self
            elif self.operator == '/':
                self.value = self.term_a.value / self.term_b.value
                self.unit = self.term_a.unit / self.term_b.unit
                return self
            elif self.operator == '^':
                self.value = math.pow(self.term_a.value, self.term_b.value)
                self.unit = self.term_a.unit
                return self
