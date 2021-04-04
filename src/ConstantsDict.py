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
        self.dictionary = self.CreateDictionary(filepath)

        for key in self.dictionary:
            print(key, self.dictionary[key])

    def CreateDictionary(self, filepath):
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

        return dictionary

    def LookupConst(text):
        """
        in:
            text - string containing the constant to evaluate
        
        out:
            (value, unit_str)
            value - float with numeric value of constant
            unit_str - string to pass into unit.from_string()
        """
