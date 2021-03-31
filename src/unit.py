
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

        index = self.getIndexOutOfBrackets('*', unit_text)
        if index != -1:
            self.operator = "*"
            self.term_a = Unit(unit_text[0:index])
            self.term_b = Unit(unit_text[index + 1::])
            return

        index = self.getIndexOutOfBrackets('/', unit_text)
        if index != -1:
            self.operator = "/"
            self.term_a = Unit(unit_text[0:index])
            self.term_b = Unit(unit_text[index + 1::])
            return

        index = self.getIndexOutOfBrackets('^', unit_text)
        if index != -1:
            self.operator = "^"
            self.term_a = Unit(unit_text[0:index])
            self.term_b = Unit(unit_text[index + 1::])
            return

    # endregion

    def __init__(self, unit_text):
        unit_text = unit_text.replace(' ', '')

        # definition of members
        self.unit_text = None
        self.operator = None
        self.term_a = None
        self.term_b = None

        # [s, m, kg, A, mol, cd]
        self.si_representation = []

        self.parse(unit_text)

    def __init__(self, si_representation):
        self.si_representation = si_representation

    def evaluate(self):
        if not self.operator:
            return self.unit_text
        else:
            if self.operator == '*':
                pass
            elif self.operator == '/':
                pass

    def __mul__(self, other):
        return Unit([x + y for x, y in zip(self, other)])

    def __truediv__(self, other):
        # TODO
        return self

    def __eq__(self, other):
        # TODO
        return True

    def __str__(self):
        # TODO
        return 'ich bin eine tolle einheit hihi'



