class SIConverter:

    def __init__(self, filepath):
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

    def SIToUnit(self, si_rep_string):
        """
        si_rep_string: comma-separated exponents of si-units (s,m,kg,A,K,mol,cd)
        """

        si_rep_ints = []
        si_rep_string = row[2].split(",")

        for string_val in si_rep_string:
            si_rep_ints.append(int(string_val))

        solutions = []
        maxTries = 5

        #MAXTRIES VERSUCHE, "PASSENDERE" EINHEITEN ZU FINDEN, BEVOR SI-DARSTELLUNG VERWENDET WIRD
        for attempt in range(maxTries):            
            record_val = -1
            record_unit = -1

            #FINDE AM BESTEN PASSENDSTE EINHEIT
            for unit in self.dictionary:
                dotprod = 0
                si_vec = self.dictionary[unit]

                for i in range(len(si_vec)):
                    dotprod += si_vec[i] * si_rep_ints[i]

                if abs(dotprod) > record_val:
                    record_val = abs(dotprod)
                    record_unit = unit

            #MINIMIERE DEN RESTLICHEN DARZUSTELLENDEN VEKTOR
            tvals = [-5,-4,-3,-2,-1,0,1,2,3,4,5]
            best_unit_sivec = self.dictionary[record_unit]

            min_length = 1000000
            min_t = 1000000

            for t in tvals:
                length_sq = 0

                for i in range(len(best_unit_sivec)):
                    length_sq += (si_rep_ints[i] - t * best_unit_sivec[i])

                if length_sq < min_length:
                    min_t = t
            
            for i in range(len(best_unit_sivec)):
                    si_rep_ints[i] = (si_rep_ints[i] - t * best_unit_sivec[i])
                

                


            




