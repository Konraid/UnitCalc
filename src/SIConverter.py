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
        
        #TESTE, OB IDENTITÄTS-EINHEIT VORLIEGT
        skip_the_whole_thing = True
        for val in si_rep_ints_copy:
            if val != 0:
                skip_the_whole_thing = False
        if(skip_the_whole_thing):
            return ""

        #MAXTRIES VERSUCHE, "PASSENDERE" EINHEITEN ZU FINDEN, BEVOR SI-DARSTELLUNG VERWENDET WIRD
        for attempt in range(maxTries):            
            record_val = -1
            record_unit = -1

            #FINDE AM BESTEN PASSENDSTE EINHEIT
            for unit in self.dictionary:
                dotprod = 0
                si_vec = self.dictionary[unit][1]
                si_vec_norm = copy.deepcopy(si_vec)

                #NORMIERTEN VEKTOR ERZEUGEN
                si_vec_length_sq = 0
                for val in si_vec:
                    si_vec_length_sq += val**2

                for i in range(len(si_vec)):
                    si_vec_norm[i] = si_vec[i]/((si_vec_length_sq)**(1/2))

                #SKALARPRODUKT BERECHNEN
                for i in range(len(si_vec)):
                    dotprod += si_vec_norm[i] * si_rep_ints_copy[i]

                if abs(dotprod) > record_val:
                    record_val = abs(dotprod)
                    record_unit = unit

            #MINIMIERE DEN RESTLICHEN DARZUSTELLENDEN VEKTOR
            #TODO: NICHT WIEDERHOLT (BEI UNTERSCHIEDLICHEN "ATTEMPTS" DIESELBE EINHEIT 0-MAL ABZIEHEN)
            record_unit_sivec = self.dictionary[record_unit][1]

            min_length = 1000000
            min_t = 1000000

            for t in range(-abs(max_exponent), abs(max_exponent)+1):
                length_sq = 0

                for i in range(len(record_unit_sivec)):
                    length_sq += (si_rep_ints_copy[i] - t * record_unit_sivec[i])**2

                if length_sq < min_length:
                    min_t = t
                    min_length = length_sq
            
            for i in range(len(record_unit_sivec)):
                    si_rep_ints_copy[i] = (si_rep_ints_copy[i] - min_t * record_unit_sivec[i])
        
            #FÜGE ENTSPRECHENDE EINHEIT ZUM LÖSUNGSVEKTOR HINZU
            solution += " * " + record_unit + "^(" + str(min_t) + ")"

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
            s = ""
            units = ['s', 'm', 'kg', 'A', 'K', 'mol', 'cd']
            for i in range(len(units)):
                if l[i] != 0:
                    x = l[i]
                    if int(x) - x == 0:
                        x = int(x)
                    s += " * " +units[i] + "^(" + str(x) + ")"
            return s[3::]
            
                

                


            




