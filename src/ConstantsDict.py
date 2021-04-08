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
            addDict = {row[0]: [row[1], row[2], row[3]]}
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

        value = float(self.dictionary[text][1])
        unit_str = self.dictionary[text][2]
        print("Used " + text + ": ", self.dictionary[text])

        return (value, unit_str)

    def AddTempConstant(self, text):
        """
        in:
            text - string in the format of "smybol ; Description ; Value ; Unit"
        """
        buffer = text.split(";")

        addDict = {buffer[0]: [buffer[1],buffer[2],buffer[3]]}
        self.dictionary.update(addDict)

