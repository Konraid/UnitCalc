class ConstantsDict:

    __instance = None

    @staticmethod
    def getInstance():
        if ConstantsDict.__instance is None:
            ConstantsDict()
        return ConstantsDict.__instance

    def __init__(self):
        if ConstantsDict.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ConstantsDict.__instance = self

        filepath = 'Constants.txt'

        self.dictionary = None
        self.InitDictionary(filepath)

        # for key in self.dictionary:
        #     print(key, self.dictionary[key])

    def InitDictionary(self, filepath):
        lookup = open(filepath, "r")

        dictionary = {}
        buffer = []

        lines = lookup.read().splitlines()
        for line in lines:
            if(line[0] != "#"):
                line = line.replace(" ", "")
                line = line.replace("\t", "")
                buffer.append(line.split(";"))

        for row in buffer:
            addDict = {row[0]: [row[1], float(row[2]), row[3]]}
            dictionary.update(addDict)

        self.dictionary = dictionary

    def LookupConst(self, text):
        """
        in:
            text - string containing the constant to evaluate
        
        out:
            (value, unit_str)
            value - float with numeric value of constant
            unit_str - string to pass into unit.from_string()
        """

        value = self.dictionary[text][1]
        unit_str = self.dictionary[text][2]
        print("Used " + text + ": ", self.dictionary[text])

        return (value, unit_str)

    def AddTempConstant(self, symbol, description, term_text):
        """
        in:
            symbol: placeholder used in equations
            description: name of the variable
            term_text: string in the format of "value[unit]" (without "")
        """

        bracket_open = term_text.find("[")
        bracket_close = term_text.find("]")
        if(bracket_close == bracket_open + 1):
            term_text = term_text.replace("[]","")
        if(bracket_open != -1):
            value = float(term_text[0:bracket_open])
            unit = term_text[bracket_open+1:bracket_close]
        else:
            value = float(term_text)
            unit = "1"

        print("Added temporary variable \"" + symbol + "\" : ", [description, value, unit])

        addDict = {symbol: [description, value, unit]}
        self.dictionary.update(addDict)

