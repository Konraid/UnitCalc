
class UnitTerm:

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

    def __init__(self, unit_text):
        #print("Created new Term with text", term_text)

        unit_text = unit_text.replace(' ', '')

        # check for correct use of parentheses
        if not self.checkNumOfBrackets(unit_text):
            print('[ERROR] Opening Brackets are not matching closing ones')
            return

        # remove redundant parentheses
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
                if bracket_counter <= 0 and i <len(unit_text) -1:
                    remove_brackets = False
                    break
        if(remove_brackets):
            unit_text = unit_text[1:-1]

        unit_text = unit_text.replace('**', '^')
        self.unit_text = unit_text


        index = self.getIndexOutOfBrackets('+', unit_text)
        if index != -1:

            self.operator = "+"
            self.termA = UnitTerm(unit_text[0:index])
            self.termB = UnitTerm(unit_text[index + 1::])
            return

        index = self.getIndexOutOfBrackets('-', unit_text)
        if index != -1:

            self.operator = "-"
            self.termA = UnitTerm(unit_text[0:index])
            self.termB = UnitTerm(unit_text[index + 1::])
            return

        index = self.getIndexOutOfBrackets('*', unit_text)
        if index != -1:
            self.operator = "*"
            self.termA = UnitTerm(unit_text[0:index])
            self.termB = UnitTerm(unit_text[index + 1::])
            return

        index = self.getIndexOutOfBrackets('/', unit_text)
        if index != -1:
            self.operator = "/"
            self.termA = UnitTerm(unit_text[0:index])
            self.termB = UnitTerm(unit_text[index + 1::])
            return

        index = self.getIndexOutOfBrackets('^', unit_text)
        if index != -1:
            self.operator = "^"
            self.termA = UnitTerm(unit_text[0:index])
            self.termB = UnitTerm(unit_text[index + 1::])
            return

    # ((T+Si+K/F) +  =m*(A-b)/c - T))

    def evaluate(self):
        if not self.operator:
            return self.unit_text
        else:
            if self.operator == '+' or self.operator == '-':
                unit_A = self.termA.evaluate()
                unit_B = self.termB.evaluate()
                if(unit_A == unit_B):
                    return unit_A
                else:
                    print('[ERROR] Units do not match in sum')
                    print('>>', self.unit_text)
            elif self.operator == '*':
                unit_A = 'm'
                unit_B = 'm^2'



    def __mul__(self, other):
        # TODO
        return self

    def __truediv__(self, other):
        # TODO
        return self

    def __eq__(self, other):
        # TODO
        return True

    def __str__(self):
        # TODO
        return 'ich bin eine tolle einheit hihi'


