import random
from colorama import Fore


def split(word):
    return [char for char in word]

def get_overlapping_pairs(string):
    ret = [] # we will return this later
    for i in range(len(string)-1): # loop through all indices except the last one
        ret.append(string[i:i+2]) # append to ret the two characters
                                  # beginning at that index
    return ret

class game:
    def __init__(self, seed, playerNo=1,difficulty=2):
        self.rng = random.Random(seed)
        self.plyrng = random.Random(seed + playerNo)
        self.won = False


        self.ingredients = ["b","a","q","l","p"]
        self.mandatoryEffects = [
        #    "1 Gold",
            "1 Brimstone Powder",
            "1 Aqua Forte",
            "1 Quicksilver",
            "1 Lead Dust",
            "1 Phosphoric Salt",
            "The Mixture has Essence of Mind",
            "The Mixture has Essence of Body",
            "The Mixture has Essence of Spirit"
        ]

        self.optionalEffects = [
            "2 Dice",
            "2 Dice",
            "2 Dice",
            "2 Dice",
            "3 Gold",
            "3 Gold",
            "6 Gold",
            "You have found Brimstone Powder has this many horizontal reactions :",
            "You have found Aqua Forte has this many horizontal reactions :",
            "You have found Quicksilver has this many horizontal reactions :",
            "You have found Lead Dust has this many horizontal reactions :",
            "You have found Phosphoric Salt has this many horizontal reactions:",
            "You have found Brimstone Powder has this many vertical reactions :",
            "You have found Aqua Forte has this many vertical reactions :",
            "You have found Quicksilver has this many vertical reactions :",
            "You have found Lead Dust has this many vertical reactions :",
            "You have found Phosphoric Salt has this many vertical reactions :"
        ]

        self.rng.shuffle(self.optionalEffects)
        self.NoptEffects=self.rng.randrange(2,7)
        self.effects = self.mandatoryEffects + self.optionalEffects[:self.NoptEffects]
        self.vValence = [0,0,0,0,0]
        self.hValence = [0, 0, 0, 0, 0]

        self.solMatrix=[
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]

        self.exMatrix=[
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]

        self.solMatrix = self.shufflesol(self.solMatrix)
        self.recipeHistory = []
        self.resultHistory = []






    def shufflesol(self,matrix):
        for effectIndex, effect in enumerate(self.effects):
            keepgoing = True
            while keepgoing:
                first = self.rng.randrange(0,5)
                second = self.rng.randrange(0, 5)
                if matrix[first][second] == 0 and matrix[second][first] == 0:
                    matrix[first][second] = effectIndex + 1
                    self.hValence[first] += 1
                    self.vValence[second] += 1
                    keepgoing = False
                    break
        return matrix



    def mix(self,recipe):
        textcolour = Fore.WHITE
        textbuffer = ""
        if recipe in self.recipeHistory:
            print("Sorry, you mixed that before. What you would get if you could mix it again:")
            textcolour = Fore.RED
        self.recipeHistory.append(recipe)
        pairs = get_overlapping_pairs(recipe)

        weakReactions = 0
        strongReactions = 0
        exhaustedReactions = 0
        products = []
        nonProducts = []
        for pair in pairs:
            first = self.ingredients.index(pair[0])
            second = self.ingredients.index(pair[1])
            if self.solMatrix[second][first] != 0 and second != first:
                weakReactions += 1
            if self.solMatrix[first][second] != 0 and self.exMatrix[first][second] == 0:
                strongReactions += 1
                products.append(self.effects[self.solMatrix[first][second] - 1])
                if self.effects[self.solMatrix[first][second] - 1] in self.optionalEffects:
                    self.exMatrix[first][second] = 1
            elif self.solMatrix[first][second] != 0 and self.exMatrix[first][second] == 1:
                exhaustedReactions += 1
                nonProducts.append(self.effects[self.solMatrix[first][second] - 1])

        wincount = 0
        if weakReactions > 0:
            textbuffer += textcolour + "There were: " + str(weakReactions) + " weak reactions.\n"
        if strongReactions > 0:
            textbuffer += textcolour + "There were: " + str(strongReactions) + " strong reactions.\n"
            random.shuffle(products)

            for p in products:
                if "Essence" in p:
                    wincount += 1
                if "vertical reactions" in p:
                    if "Brimstone Powder" in p:
                        textbuffer +="\t"+ p + str(self.vValence[0]) + "\n"
                    if "Aqua Forte" in p:
                        textbuffer +="\t"+ p + str(self.vValence[1]) + "\n"
                    if "Quicksilver" in p:
                        textbuffer +="\t"+ p + str(self.vValence[2]) + "\n"
                    if "Lead Dust" in p:
                        textbuffer +="\t"+ p + str(self.vValence[3]) + "\n"
                    if "Phosphoric Salt" in p:
                        textbuffer +="\t"+ p + str(self.vValence[4]) + "\n"
                if "horizontal reactions" in p:
                    if "Brimstone Powder" in p:
                        textbuffer +="\t"+ p + str(self.hValence[0]) + "\n"
                    if "Aqua Forte" in p:
                        textbuffer +="\t"+ p + str(self.hValence[1]) + "\n"
                    if "Quicksilver" in p:
                        textbuffer +="\t"+ p + str(self.hValence[2]) + "\n"
                    if "Lead Dust" in p:
                        textbuffer +="\t"+ p + str(self.hValence[3]) + "\n"
                    if "Phosphoric Salt" in p:
                        textbuffer +="\t"+ p + str(self.hValence[4]) + "\n"
                else:
                    textbuffer +="\t" + p + "\n"
        if exhaustedReactions > 0:
            textbuffer += textcolour + "There were: " + str(exhaustedReactions) + " Exhausted Reactions.\n"
            random.shuffle(nonProducts)
            for p in nonProducts:
                if "vertical reactions" in p:
                    if "Brimstone Powder" in p:
                        textbuffer +="\t"+ p + str(self.vValence[0]) + "\n"
                    if "Aqua Forte" in p:
                        textbuffer +="\t"+ p + str(self.vValence[1]) + "\n"
                    if "Quicksilver" in p:
                        textbuffer +="\t"+ p + str(self.vValence[2]) + "\n"
                    if "Lead Dust" in p:
                        textbuffer +="\t"+ p + str(self.vValence[3]) + "\n"
                    if "Phosphoric Salt" in p:
                        textbuffer +="\t"+ p + str(self.vValence[4]) + "\n"
                if "horizontal reactions" in p:
                    if "Brimstone Powder" in p:
                        textbuffer +="\t"+ p + str(self.hValence[0]) + "\n"
                    if "Aqua Forte" in p:
                        textbuffer +="\t"+ p + str(self.hValence[1]) + "\n"
                    if "Quicksilver" in p:
                        textbuffer +="\t"+ p + str(self.hValence[2]) + "\n"
                    if "Lead Dust" in p:
                        textbuffer +="\t"+ p + str(self.hValence[3]) + "\n"
                    if "Phosphoric Salt" in p:
                        textbuffer +="\t"+ p + str(self.hValence[4]) + "\n"
                else:
                    textbuffer +="\t" + p + "\n"
        if weakReactions == 0 and strongReactions == 0 and exhaustedReactions == 0:
            textbuffer += textcolour + "There were no reactions.\n"
        if wincount == 3:
            textbuffer += Fore.YELLOW + "You have sythesised the philosopher's stone!"
            self.won = True

        textbuffer +="\n"
        self.resultHistory.append(textbuffer)

    def getLastRecipe(self):
        return self.recipeHistory[-1]

    def getLastResult(self):
        return self.resultHistory[-1]

    def getRecipeHistory(self):
        self.recipeHistory

    def getResultsHistory(self):
        return self.resultHistory

    def getSolution(self):
        textbuffer=''
        textbuffer+="solution:\n"
        for n in self.solMatrix:
            textbuffer+= str(n) + "\n"
        i = 1
        for n in self.effects:
            textbuffer+= str(i) + ": " + n + "\n"
            i += 1
        return textbuffer











