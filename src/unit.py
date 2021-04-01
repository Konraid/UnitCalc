from SIConverter import SIConverter


class Unit:

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

    #IDENTITÄT, FALLS unit_text = ""
    def __init__(self, unit_text, rep):
        # region MEMBER DEFINITION
        self.unit_text = None
        self.operator = None
        self.unit_a = None
        self.unit_b = None
        self.si_representation = None #[s, m, kg, A, K, mol, cd]
        # endregion

        if unit_text != None:
            if unit_text != "":
                unit_text = unit_text.replace(' ', '')
                unit_text = unit_text.replace('**', '^')

                # region KLAMMERSETZUNG PRÜFEN
                if not self.checkNumOfBrackets(unit_text):
                    print('[ERROR] Opening Brackets are not matching closing ones')
                    return
                # endregion

                # region ÜBERFLÜSSIGE KLAMMERN ENTFERNEN
                remove_brackets = True
                while(remove_brackets):
                    remove_brackets = False
                    bracket_counter = 1
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
                # endregion

                # region (SUB)UNITS UNTERSCHEIDEN
                index = self.getIndexOutOfBrackets('*', unit_text)
                if index != -1:
                    self.operator = "*"
                    self.unit_a = Unit.from_string(unit_text[0:index])
                    self.unit_b = Unit.from_string(unit_text[index + 1::])
                else:
                    index = self.getIndexOutOfBrackets('/', unit_text)
                    if index != -1:
                        self.operator = "/"
                        self.unit_a = Unit.from_string(unit_text[0:index])
                        self.unit_b = Unit.from_string(unit_text[index + 1::])
                    else:
                        index = self.getIndexOutOfBrackets('^', unit_text)
                        if index != -1:
                            self.operator = "^"
                            self.unit_a = Unit.from_string(unit_text[0:index])
                            self.unit_b = Unit.from_string(unit_text[index + 1::])
            # endregion

                self.unit_text = unit_text
                self.evaluate_to_SI()

            else:
                # IDENTITÄT
                self.unit_text = ""
                self.si_representation = [0,0,0,0,0,0,0]
        else:
            if rep != None:
                self.si_representation = rep
                #TODO: TEXT ERZEUGEN AUS REP
            else:
                print("[Error] unit_text and rep both set to None")

    # ERZEUGE SI-REPRÄSENTATION
    def evaluate_to_SI(self):
        if self.si_representation == None:
            if not hasattr(self, 'operator') or self.operator is None:
                # region INNERSTE STUFE
                # FALLS unit_text ALS int INTERPRETIERT WERDEN KANN (Z.B. '1' in [1/m]),
                #   LIEGT KEINE "ECHTE" EINHEIT VOR
                self.si_representation = [0,0,0,0,0,0,0]
                try:
                    i = int(self.unit_text)
                except ValueError:
                    # FALLS INTERPRETATION ALS int FEHLSCHLÄGT, WERTE unit_text MITTELS TABELLE AUS
                    self.si_representation = SIConverter.getInstance().UnitToSI(self.unit_text)[1]
                # endregion
            else:
                # region BESTIMMUNG AUS SUBEINHEITEN
                self.unit_a.evaluate_to_SI()
                self.unit_b.evaluate_to_SI()
                if self.operator == '*':
                    self.si_representation = (self.unit_a * self.unit_b).si_representation
                elif self.operator == '/':
                    self.si_representation = (self.unit_a / self.unit_b).si_representation
                elif self.operator == '^':
                    self.si_representation = (self.unit_a**float(self.unit_b.unit_text)).si_representation
                # endregion

    # region KONSTRUKTOR-ERSATZ
    @classmethod
    def from_representation(cls, rep):
        return cls(None, rep)

    @classmethod
    def from_string(cls, unit_text):
        return cls(unit_text, None)

    @classmethod
    def identity(cls):
        return cls("", [0,0,0,0,0,0,0])
    # endregion

    # region OPERATORDEFINITIONEN MITTELS SI-REPRÄSENTATION
    def __mul__(self, other):
        return Unit.from_representation([x + y for x, y in zip(self.si_representation, other.si_representation)])

    def __truediv__(self, other):
        return Unit.from_representation([x - y for x, y in zip(self.si_representation, other.si_representation)])

    def __eq__(self, other):
        return self.si_representation == other.si_representation

    def __pow__(self, other):
        return Unit.from_representation([self.si_representation[i] * other for i in range(len(self.si_representation))])

    def __str__(self):
        l = self.si_representation
        # [s, m, kg, A, K, mol, cd]
        s = ""
        units = ['s', 'm', 'kg', 'A', 'K', 'mol', 'cd']
        for i in range(len(units)):
            if l[i] != 0:
                x = l[i]
                if int(x) - x == 0:
                    x = int(x)
                s += " * " +units[i] + "^(" + str(x) + ")"
        return s[3::]
    # endregion



