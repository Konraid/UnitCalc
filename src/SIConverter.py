class SIConverter:

    def __init__(self, filepath):
        self.dictionary = self.CreateDictionary(filepath)

        for key in self.dictionary:
            print(key, self.dictionary[key])

    def CreateDictionary(self, filepath):
        lookup = open(filepath, "r")

        dictionary = {}
        buffer = []

        lines = lookup.read().splitlines()
        for line in lines:
            line = line.replace(" ", "")
            line = line.replace("\t", "")
            buffer.append(line.split(";"))

        titles = buffer.pop(0)

        for row in buffer:
            addDict = {row[0]: [row[1], row[2]]}
            dictionary.update(addDict)

        return dictionary


    def UnitToSI(unit_string):
        return self.dictionary[unit_string]

    def SIToUnit():
        a = 1
