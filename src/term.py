from unit import Unit
import math


class TermParser:
    def getIndexOutOfBrackets(self, symbol, string):
        """
        finds index of a symbol (-->operator) outside of a (...)-context
        """
        bracket_counter = 0
        hard_bracket_counter = 0
        for i in range(0, len(string)):
            s = string[i]
            if s == '(':
                bracket_counter += 1
            elif s == ')':
                bracket_counter -= 1
            elif s == '[':
                hard_bracket_counter += 1
            elif s == ']':
                hard_bracket_counter -= 1
            if s == symbol and bracket_counter == 0 and hard_bracket_counter == 0:
                return i
        return -1

    def checkNumOfBrackets(self, string):
        bracket_counter = 0
        hard_bracket_counter = 0
        for i in range(0, len(string)):
            s = string[i]
            if s == '(':
                bracket_counter += 1
            elif s == ')':
                bracket_counter -= 1
            elif s == '[':
                hard_bracket_counter += 1
            elif s == ']':
                hard_bracket_counter -= 1
        return bracket_counter == 0 and hard_bracket_counter == 0

    def __init__(self, term_text):
        term_text = term_text.replace(' ', '')
        term_text = term_text.replace('**', '^')

        # region MEMBER DEFINITION
        self.unit = None
        self.value = None
        self.term_text = None
        self.operator = None
        self.term_a = None
        self.term_b = None
        # endregion

        # region KLAMMERSETZUNG PRÜFEN
        if not self.checkNumOfBrackets(term_text):
            print('[ERROR] Opening Brackets are not matching closing ones')
            return
        # endregion

        # region ÜBERFLÜSSIGE KLAMMERN ENTFERNEN
        remove_brackets = True
        while (remove_brackets):
            remove_brackets = False
            bracket_counter = 1
            if term_text.startswith('(') and term_text.endswith(')'):
                remove_brackets = True
                for i in range(1, len(term_text)):
                    s = term_text[i]
                    if s == '(':
                        bracket_counter += 1
                    elif s == ')':
                        bracket_counter -= 1
                    if bracket_counter <= 0 and i < len(term_text) - 1:
                        remove_brackets = False
                        break
            if (remove_brackets):
                term_text = term_text[1:-1]
        # endregion

        # region (SUB)TERME UNTERSCHEIDEN
        # PUNKT VOR STRICH --> INNERSTE STRUKTUREN SIND PRODUKTE/QUOTIENTEN/...
        index = self.getIndexOutOfBrackets('+', term_text)
        if index != -1:
            self.operator = "+"
            self.term_a = TermParser(term_text[0:index])
            self.term_b = TermParser(term_text[index + 1::])
        else:
            index = self.getIndexOutOfBrackets('-', term_text)
            if index != -1:
                self.operator = "-"
                self.term_a = TermParser(term_text[0:index])
                self.term_b = TermParser(term_text[index + 1::])
            else:
                index = self.getIndexOutOfBrackets('*', term_text)
                if index != -1:
                    self.operator = "*"
                    self.term_a = TermParser(term_text[0:index])
                    self.term_b = TermParser(term_text[index + 1::])
                else:
                    index = self.getIndexOutOfBrackets('/', term_text)
                    if index != -1:
                        self.operator = "/"
                        self.term_a = TermParser(term_text[0:index])
                        self.term_b = TermParser(term_text[index + 1::])
                    else:
                        index = self.getIndexOutOfBrackets('^', term_text)
                        if index != -1:
                            self.operator = "^"
                            self.term_a = TermParser(term_text[0:index])
                            self.term_b = TermParser(term_text[index + 1::])
                        else:
                            if term_text.startswith("exp("):
                                self.operator = "exp"
                                self.term_a = TermParser(term_text[4:-1:])
                            else:
                                if term_text.startswith("ln("):
                                    self.operator = "ln"
                                    self.term_a = TermParser(term_text[3:-1:])
                                else:
                                    if term_text.startswith("sin("):
                                        self.operator = "sin"
                                        self.term_a = TermParser(term_text[4:-1:])
                                    else:
                                        if term_text.startswith("cos("):
                                            self.operator = "cos"
                                            self.term_a = TermParser(term_text[4:-1:])
                                        else:
                                            if term_text.startswith("tan("):
                                                self.operator = "tan"
                                                self.term_a = TermParser(term_text[4:-1:])
                                            else:
                                                if term_text.startswith("arcsin("):
                                                    self.operator = "arcsin"
                                                    self.term_a = TermParser(term_text[7:-1:])
                                                else:
                                                    if term_text.startswith("arccos("):
                                                        self.operator = "arccos"
                                                        self.term_a = TermParser(term_text[7:-1:])
                                                    else:
                                                        if term_text.startswith("arctan("):
                                                            self.operator = "arctan"
                                                            self.term_a = TermParser(term_text[7:-1:])
                                                        else:
                                                            if term_text.startswith("sinh("):
                                                                self.operator = "sinh"
                                                                self.term_a = TermParser(term_text[5:-1:])
                                                            else:
                                                                if term_text.startswith("cosh("):
                                                                    self.operator = "cosh"
                                                                    self.term_a = TermParser(term_text[5:-1:])
                                                                else:
                                                                    if term_text.startswith("tanh("):
                                                                        self.operator = "tanh"
                                                                        self.term_a = TermParser(term_text[5:-1:])
                                                                    else:
                                                                        if term_text.startswith("arsinh("):
                                                                            self.operator = "arcinh"
                                                                            self.term_a = TermParser(term_text[7:-1:])
                                                                        else:
                                                                            if term_text.startswith("arcosh("):
                                                                                self.operator = "arcosh"
                                                                                self.term_a = TermParser(
                                                                                    term_text[7:-1:])
                                                                            else:
                                                                                if term_text.startswith("artanh("):
                                                                                    self.operator = "artanh"
                                                                                    self.term_a = TermParser(
                                                                                        term_text[7:-1:])

        # endregion

        self.term_text = term_text
        self.evaluate()

    # ERZEUGE INHALT  
    def evaluate(self):
        if not hasattr(self, 'operator') or self.operator is None:
            # region INNERSTE/UNTERSTE STUFE ERREICHT, term = value[unit]
            if '[' in self.term_text:
                unit_starts = self.term_text.find('[')
                self.value = float(self.term_text[:unit_starts])
                self.unit = Unit.from_string(self.term_text[unit_starts + 1:-1:])
            else:
                try:
                    self.value = float(self.term_text)
                except ValueError:
                    # text is a constant
                    self.value = 1
                self.unit = Unit.identity()
            return self
            # endregion
        else:
            # region BESTIMME TERM AUS SUBTERMEN
            if (self.term_a != None):
                self.term_a.evaluate()
            if (self.term_b != None):
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
                    print('=======[ERROR]=======> Units do not match in sum.')
                    print('>>', self.term_text)
                    self.value = 0
                    self.unit = Unit.identity()
                return self

            elif self.operator == '*':
                self.value = self.term_a.value * self.term_b.value
                self.unit = self.term_a.unit * self.term_b.unit
                return self

            elif self.operator == '/':
                self.value = self.term_a.value / self.term_b.value
                self.unit = self.term_a.unit / self.term_b.unit
                return self

            elif self.operator == '^':
                if self.term_b.unit == Unit.identity():
                    self.value = math.pow(self.term_a.value, self.term_b.value)
                    self.unit = self.term_a.unit ** self.term_b.value
                else:
                    print('=======[ERROR]=======> Exponents cant have units.')
                    print('>>', self.term_text)
                    self.value = 0
                    self.unit = Unit.identity()
                return self

            elif self.operator == "exp":
                if self.term_a.unit == Unit.identity():
                    self.value = math.exp(self.term_a.value)
                    self.unit = Unit.identity()
                else:
                    print('=======[ERROR]=======> Exponents cant have units.')
                    print('>>', self.term_text)
                    self.value = 0
                return self

            elif self.operator == "ln":
                if self.term_a.unit == Unit.identity():
                    self.value = math.log(self.term_a.value, math.e)
                    self.unit = Unit.identity()
                else:
                    print('=======[ERROR]=======> Arguments of logs cant have units.')
                    print('>>', self.term_text)
                    self.value = 0
                    self.unit = Unit.identity()
                return self

            elif self.operator == "sin":
                if self.term_a.unit == Unit.identity():
                    self.value = math.sin(self.term_a.value)
                    self.unit = Unit.identity()
                else:
                    print('=======[ERROR]=======> Arguments of trig functions cant have units.')
                    print('>>', self.term_text)
                    self.value = 0
                    self.unit = Unit.identity()
                return self

            elif self.operator == "cos":
                if self.term_a.unit == Unit.identity():
                    self.value = math.cos(self.term_a.value)
                    self.unit = Unit.identity()
                else:
                    print('=======[ERROR]=======> Arguments of trig functions cant have units.')
                    print('>>', self.term_text)
                    self.value = 0
                    self.unit = Unit.identity()
                return self

            elif self.operator == "tan":
                if self.term_a.unit == Unit.identity():
                    self.value = math.tan(self.term_a.value)
                    self.unit = Unit.identity()
                else:
                    print('=======[ERROR]=======> Arguments of trig functions cant have units.')
                    print('>>', self.term_text)
                    self.value = 0
                    self.unit = Unit.identity()
                return self

            elif self.operator == "arcsin":
                if self.term_a.unit == Unit.identity():
                    self.value = math.asin(self.term_a.value)
                    self.unit = Unit.identity()
                else:
                    print('=======[ERROR]=======> Arguments of inverse trig functions cant have units.')
                    print('>>', self.term_text)
                    self.value = 0
                    self.unit = Unit.identity()
                return self

            elif self.operator == "arccos":
                if self.term_a.unit == Unit.identity():
                    self.value = math.acos(self.term_a.value)
                    self.unit = Unit.identity()
                else:
                    print('=======[ERROR]=======> Arguments of inverse trig functions cant have units.')
                    print('>>', self.term_text)
                    self.value = 0
                    self.unit = Unit.identity()
                return self

            elif self.operator == "arctan":
                if self.term_a.unit == Unit.identity():
                    self.value = math.atan(self.term_a.value)
                    self.unit = Unit.identity()
                else:
                    print('=======[ERROR]=======> Arguments of inverse trig functions cant have units.')
                    print('>>', self.term_text)
                    self.value = 0
                    self.unit = Unit.identity()
                return self

            elif self.operator == "sinh":
                if self.term_a.unit == Unit.identity():
                    self.value = math.sinh(self.term_a.value)
                    self.unit = Unit.identity()
                else:
                    print('=======[ERROR]=======> Arguments of hyperbolic trig functions cant have units.')
                    print('>>', self.term_text)
                    self.value = 0
                    self.unit = Unit.identity()
                return self

            elif self.operator == "cosh":
                if self.term_a.unit == Unit.identity():
                    self.value = math.cosh(self.term_a.value)
                    self.unit = Unit.identity()
                else:
                    print('=======[ERROR]=======> Arguments of hyperbolic trig functions cant have units.')
                    print('>>', self.term_text)
                    self.value = 0
                    self.unit = Unit.identity()
                return self

            elif self.operator == "tanh":
                if self.term_a.unit == Unit.identity():
                    self.value = math.tanh(self.term_a.value)
                    self.unit = Unit.identity()
                else:
                    print('=======[ERROR]=======> Arguments of hyperbolic trig functions cant have units.')
                    print('>>', self.term_text)
                    self.value = 0
                    self.unit = Unit.identity()
                return self

            elif self.operator == "arsinh":
                if self.term_a.unit == Unit.identity():
                    self.value = math.asinh(self.term_a.value)
                    self.unit = Unit.identity()
                else:
                    print('=======[ERROR]=======> Arguments of inverse hyperbolic trig functions cant have units.')
                    print('>>', self.term_text)
                    self.value = 0
                    self.unit = Unit.identity()
                return self

            elif self.operator == "arcosh":
                if self.term_a.unit == Unit.identity():
                    self.value = math.acosh(self.term_a.value)
                    self.unit = Unit.identity()
                else:
                    print('=======[ERROR]=======> Arguments of inverse hyperbolic trig functions cant have units.')
                    print('>>', self.term_text)
                    self.value = 0
                    self.unit = Unit.identity()
                return self

            elif self.operator == "artanh":
                if self.term_a.unit == Unit.identity():
                    self.value = math.atanh(self.term_a.value)
                    self.unit = Unit.identity()
                else:
                    print('=======[ERROR]=======> Arguments of inverse hyperbolic trig functions cant have units.')
                    print('>>', self.term_text)
                    self.value = 0
                    self.unit = Unit.identity()
                return self

            # endregion