from SIConverter import SIConverter


class Unit:

    # region Parser
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

    def parse(self, unit_text):
        # check for correct use of parentheses
        if not self.checkNumOfBrackets(unit_text):
            print('[ERROR] Opening Brackets are not matching closing ones')
            return

        # region remove redundant parentheses
        bracket_counter = 1
        remove_brackets = False
        if unit_text.startswith('(') and unit_text.endswith(')'):
            remove_brackets = True
            for i in range(1, len(unit_text)):
                s = unit_text[i]
                if s == '(':
                    bracket_counter += 1
                elif s == ')':
                    bracket_counter -= 1
                if bracket_counter <= 0 and i < len(unit_text) - 1:
                    remove_brackets = False
                    break
        if (remove_brackets):
            unit_text = unit_text[1:-1]
        # endregion

        unit_text = unit_text.replace('**', '^')
        self.unit_text = unit_text

        index = self.getIndexOutOfBrackets('^', unit_text)
        if index != -1:
            self.operator = "^"
            self.term_a = Unit.with_string(unit_text[0:index])
            self.term_b = Unit.with_string(unit_text[index + 1::])
            return

        index = self.getIndexOutOfBrackets('*', unit_text)
        if index != -1:
            self.operator = "*"
            self.term_a = Unit.with_string(unit_text[0:index])
            self.term_b = Unit.with_string(unit_text[index + 1::])
            return

        index = self.getIndexOutOfBrackets('/', unit_text)
        if index != -1:
            self.operator = "/"
            self.term_a = Unit.with_string(unit_text[0:index])
            self.term_b = Unit.with_string(unit_text[index + 1::])
            return

    # endregion

    def __init__(self, unit_text, rep, eval):
        unit_text = unit_text.replace(' ', '')

        # definition of members
        self.unit_text = None
        self.operator = None
        self.term_a = None
        self.term_b = None

        # [s, m, kg, A, K, mol, cd]
        self.si_representation = rep
        if not rep:
            self.parse(unit_text)
        if eval:
            self.evaluate()

    @classmethod
    def with_representation(cls, rep):
        return cls("", rep, False)

    @classmethod
    def with_string(cls, unit_text, eval=False):
        return cls(unit_text, [], eval)

    @classmethod
    def identity(cls):
        return cls("", [0,0,0,0,0,0,0], False)

    def evaluate(self):
        if not hasattr(self, 'operator') or self.operator is None:
            # TODO GET SI REP
            self.si_representation = SIConverter.getInstance().UnitToSI(self.unit_text)[1]
        else:
            self.term_a.evaluate()
            self.term_b.evaluate()
            if self.operator == '*':
                self.si_representation = (self.term_a * self.term_b).si_representation
            elif self.operator == '/':
                self.si_representation = self.term_a / self.term_b
            elif self.operator == '^':
                self.si_representation = self.term_a**float(self.term_b.unit_text)

    def __mul__(self, other):
        return Unit.with_representation([x + y for x, y in zip(self.si_representation, other.si_representation)])

    def __truediv__(self, other):
        return Unit.with_representation([x - y for x, y in zip(self.si_representation, other.si_representation)])

    def __eq__(self, other):
        return self.si_representation == other.si_representation

    def __pow__(self, other):
        return Unit.with_representation([self.si_representation[i] * other for i in range(len(self.si_representation))])

    def __str__(self):
        l = self.si_representation
        # [s, m, kg, A, K, mol, cd]
        s = ""
        units = ['s', 'm', 'kg', 'A', 'K', 'mol', 'cd']
        for i in range(len(units)):
            if l[i] != 0:
                s += units[i] + '^' + str(l[i])
        return s



