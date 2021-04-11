import copy

class SIConverter:

    __instance = None

    @staticmethod
    def getInstance():
        if SIConverter.__instance is None:
            SIConverter()
        return SIConverter.__instance

    def __init__(self):
        if SIConverter.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            SIConverter.__instance = self

        filepath = 'UnitsSI.txt'
        self.dictionary = self.CreateDictionary(filepath)

        # for key in self.dictionary:
        #     print(key, self.dictionary[key])

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
            si_rep_ints = []
            si_rep_string = row[2].split(",")

            for string_val in si_rep_string:
                si_rep_ints.append(int(string_val))

            addDict = {row[0]: [row[1], si_rep_ints]}
            dictionary.update(addDict)

        return dictionary


    def UnitToSI(self, unit_string):
        return self.dictionary[unit_string]

    def SIToUnit(self, si_rep_ints, max_tries, max_exponent):
        """
        si_rep_ints: list of int exponents (s,m,kg,A,K,mol,cd)
        max_tries: maximum number of different "base" units
        max_exponent: highest absolute exponent value (eg. m⁴)
        """

        foundSolution = False
        solution = ""
        maxTries = max_tries
        si_rep_ints_copy = copy.deepcopy(si_rep_ints)
        bad_candidates = []
        
        #TESTE, OB IDENTITÄTS-EINHEIT VORLIEGT
        skip_the_whole_thing = True
        for val in si_rep_ints_copy:
            if val != 0:
                skip_the_whole_thing = False
        if(skip_the_whole_thing):
            return ""

        for attempt in range(maxTries):
            
            record_length_sq = 10000000
            record_t = None
            record_unit = None

            for unit in self.dictionary:
                current_si_vec = self.dictionary[unit][1]

                for t in range(-abs(max_exponent), abs(max_exponent)+1):
                    current_resid_length_sq = 0

                    for i in range(len(current_si_vec)):
                        current_resid_length_sq += (si_rep_ints_copy[i] - t * current_si_vec[i])**2

                    if current_resid_length_sq < record_length_sq:
                        record_length_sq = current_resid_length_sq
                        record_t = t
                        record_unit = unit

            for j in range(len(si_rep_ints_copy)):
                si_rep_ints_copy[j] -= record_t * self.dictionary[record_unit][1][j]
            
            solution += " * " + record_unit + "^(" + str(record_t) + ")"

            #TESTE, OB RESTVEKTOR BEREITS 0 IST
            isZero = True
            for val in si_rep_ints_copy:
                if val != 0:
                    isZero = False
            if(isZero):
                foundSolution = True
                break
        
        if(foundSolution):
            return solution[3::]
        else:
            print("didn't find a good solution")
            s = ""
            units = ['s', 'm', 'kg', 'A', 'K', 'mol', 'cd']
            for i in range(len(units)):
                if si_rep_ints[i] != 0:
                    x = si_rep_ints[i]
                    if int(x) - x == 0:
                        x = int(x)
                    s += " * " + units[i] + "^(" + str(x) + ")"
            return s[3::]
            
                

                


            




