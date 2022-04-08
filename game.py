import random


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
        self.gameSeed=seed
        self.rng = random.Random(seed)
        self.plyrng = random.Random(seed + playerNo)
        self.won = False
        self.difficulty = int(difficulty)

        self.textColour = '#000000'


        self.ingredients = ["n","a","q","l","p"]
        self.ingredientsLongnames = ["Nitre Powder", "Aqua Fortis", "Quicksilver", "Lead Dust", "Phosphoric Salt"]
        self.domains = ["Jupiter", "Mars", "Sol", "Venus", "Saturn"]

        self.mandatoryEffects = [
            "3 Nitre Powder",
            "3 Aqua Fortis",
            "3 Quicksilver",
            "3 Lead Dust",
            "3 Phosphoric Salt",
            "The Mixture has Essence of Mind",
            "The Mixture has Essence of Body",
            "The Mixture has Essence of Spirit"
        ]

        self.bonusEffects = [
            "2 Dice",
            "2 Dice",
            "2 Dice",
            "2 Dice",
            "2 Dice",
            "2 Dice",
            "3 Gold",
            "3 Gold",
            "3 Gold",
            "3 Gold",
            "3 Gold",
            "3 Gold",
            "5 Gold",
            "5 Gold",
            "5 Gold"
        ]

        self.informationEffects = [
            "You have found Nitre Powder has {} horizontal reactions",
            "You have found Aqua Forte has {} horizontal reactions",
            "You have found Quicksilver has {} horizontal reactions",
            "You have found Lead Dust has {} horizontal reactions",
            "You have found Phosphoric Salt has {} horizontal reactions",
            "You have found Nitre Powder has {} vertical reactions",
            "You have found Aqua Forte has {} vertical reactions",
            "You have found Quicksilver has {} vertical reactions",
            "You have found Lead Dust has {} vertical reactions",
            "You have found Phosphoric Salt has {} vertical reactions",
            "The Mind can be found in the Domain of {}",
            "The Spirit can be found in the Domain of {}",
            "The Body can be found in the Domain of {}",
            "The Domain of Jupiter has {} reactions",
            "The Domain of Saturn has {} reactions",
            "The Domain of Mars has {} reactions",
            "The Domain of Venus has {} reactions",
            "The Domain of Sol has {} reactions",
            "The Mind can be found in the Domain of {}",
            "The Spirit can be found in the Domain of {}",
            "The Body can be found in the Domain of {}",
            "The Mind requires a quantity of {}",
            "The Spirit requires a quantity of {}",
            "The Body requires a quantity of {}"
        ]

        self.optionalEffects = self.bonusEffects[:] + self.informationEffects[:]
        self.rng.shuffle(self.optionalEffects)
        self.NoptEffects=self.rng.randrange(2,6)
        self.effects = self.mandatoryEffects[:] + self.optionalEffects[:self.NoptEffects]
        self.vValence = [0,0,0,0,0]
        self.hValence = [0, 0, 0, 0, 0]

        self.solMatrix=[
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]

        self.domainMask = [
            [0, 0, 0, 1, 1],
            [0, 0, 2, 1, 1],
            [3, 2, 2, 2, 1],
            [3, 3, 2, 4, 4],
            [3, 3, 4, 4, 4]
        ]

        self.domainMatrix=[
            [],
            [],
            [],
            [],
            []
        ]

        self.exMatrix=[
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]

        self.solMatrix = self.shufflesol(self.solMatrix)
        self.recipeHistory = [""]
        self.resultHistory = [""]
        self.startingFacts = []

        #setup starting facts
        self.setupStartingFacts()



    def strongRactionResulttoBuffer(self,p,textbuffer):
        if "vertical reactions" in p:
            if "Nitre Powder" in p:
                textbuffer += "\t" + p.format(self.vValence[0]) + "\n"
            if "Aqua Forte" in p:
                textbuffer += "\t" + p.format(self.vValence[1]) + "\n"
            if "Quicksilver" in p:
                textbuffer += "\t" + p.format(self.vValence[2]) + "\n"
            if "Lead Dust" in p:
                textbuffer += "\t" + p.format(self.vValence[3]) + "\n"
            if "Phosphoric Salt" in p:
                textbuffer += "\t" + p.format(self.vValence[4]) + "\n"
        elif "horizontal reactions" in p:
            if "Nitre Powder" in p:
                textbuffer += "\t" + p.format(self.hValence[0]) + "\n"
            if "Aqua Forte" in p:
                textbuffer += "\t" + p.format(self.hValence[1]) + "\n"
            if "Quicksilver" in p:
                textbuffer += "\t" + p.format(self.hValence[2]) + "\n"
            if "Lead Dust" in p:
                textbuffer += "\t" + p.format(self.hValence[3]) + "\n"
            if "Phosphoric Salt" in p:
                textbuffer += "\t" + p.format(self.hValence[4]) + "\n"
        elif "requires a quantity" in p:
            for rowindex, row in enumerate(self.solMatrix):
                for columnindex,cell in enumerate(row):
                    if "Essence of Mind" in self.effects[cell - 1] and "Mind" in p:
                        random.seed(str(self.gameSeed) + "Mind")
                        ingredient = self.ingredientsLongnames[random.choice((rowindex,columnindex))]
                        textbuffer += "\t" + p.format(ingredient) + "\n"
                        break
                    if "Essence of Body" in self.effects[cell - 1] and "Body" in p:
                        random.seed(str(self.gameSeed) + "Body")
                        ingredient = self.ingredientsLongnames[random.choice((rowindex,columnindex))]
                        textbuffer += "\t" + p.format(ingredient) + "\n"
                        break
                    if "Essence of Spirit" in self.effects[cell - 1] and "Spirit" in p:
                        random.seed(str(self.gameSeed) + "Spirit")
                        ingredient = self.ingredientsLongnames[random.choice((rowindex,columnindex))]
                        textbuffer += "\t" + p.format(ingredient) + "\n"
                        break
        elif "can be found in the Domain of" in p:
            for domainindex, domain in enumerate(self.domainMatrix):
                for cell in domain:
                    # print(domain,cell)
                    if "Essence of Mind" in self.effects[cell - 1] and "Mind" in p:
                        textbuffer += "\t" + p.format(self.domains[domainindex]) + "\n"
                        break
                    if "Essence of Body" in self.effects[cell - 1] and "Body" in p:
                        textbuffer += "\t" + p.format(self.domains[domainindex]) + "\n"
                        break
                    if "Essence of Spirit" in self.effects[cell - 1] and "Spirit" in p:
                        textbuffer += "\t" + p.format(self.domains[domainindex]) + "\n"
                        break
        elif "The Domain of " in p:
            if "Jupiter" in p:
                textbuffer += "\t" + p.format(len(self.domainMatrix[0])) + "\n"
            if "Mars" in p:
                textbuffer += "\t" + p.format(len(self.domainMatrix[1])) + "\n"
            if "Sol" in p:
                textbuffer += "\t" + p.format(len(self.domainMatrix[2])) + "\n"
            if "Venus" in p:
                textbuffer += "\t" + p.format(len(self.domainMatrix[3])) + "\n"
            if "Saturn" in p:
                textbuffer += "\t" + p.format(len(self.domainMatrix[4])) + "\n"
        else:
            textbuffer += "\t" + p + "\n"
        return textbuffer

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
                    domain=self.domainMask[first][second]
                    self.domainMatrix[domain].append(effectIndex + 1)

                    keepgoing = False
                    break
        return matrix

    def setupStartingFacts(self):
        textbuffer = ""
        if self.difficulty == 0:
            textbuffer += "You start your search with little to go on.\n"
        else:
            textbuffer += "You have Learned that:\n"
            textbuffer += "\tThere are {} exhaustible reactions.\n".format(self.NoptEffects)
            if self.difficulty >= 1:
                startingEffects = self.effects[:]
                self.plyrng.shuffle(startingEffects)
                knownEffects = startingEffects[ 0 : self.difficulty ]
                for effect in knownEffects:
                    effectindex = self.effects.index(effect) + 1
                    for row in range(0,5):
                        for column in range(0,5):
                            if effectindex == self.solMatrix[row][column]:
                                textbuffer += "\t" + self.ingredients[row] + self.ingredients[column] + " produces a strong reaction.\n"
            if self.difficulty >= 2:
                startingEffects = self.informationEffects[:]
                self.plyrng.shuffle(startingEffects)
                startingEffects = startingEffects[0 : self.difficulty-1]
                for p in startingEffects:
                    textbuffer = self.strongRactionResulttoBuffer(p, textbuffer)

        self.startingFacts = textbuffer


    def getStartingFacts(self):
        return self.startingFacts

    def mix(self,recipe):

        #0 filter out bad invalid recipies
        if len(set(split(recipe) + self.ingredients)) > len(set(self.ingredients)) or len(recipe) < 2 or len(recipe) > 6:
            print('Invalid recipe. a recipe must only contain characters n, a, q, l, or p, and must be between 2 and '
                  '6 characters long (inclusive)."')
            return
        self.textColour = '#000000'
        textbuffer = ""
        if recipe in self.recipeHistory:
            textbuffer += "Sorry, you mixed that before. You found the following last time:"
            self.textColour = '#ff0000'

        self.recipeHistory.append(recipe)
        pairs = get_overlapping_pairs(recipe)

        weakReactions = 0
        strongReactions = 0
        exhaustedReactions = 0
        products = []
        nonProducts = []

        #1 proccess reactions
        for pair in pairs:
            first = self.ingredients.index(pair[0])
            second = self.ingredients.index(pair[1])
            if self.solMatrix[second][first] != 0 and second != first:
                weakReactions += 1
            if self.solMatrix[first][second] != 0 and self.exMatrix[first][second] == 1:
                exhaustedReactions += 1
                nonProducts.append(self.effects[self.solMatrix[first][second] - 1])
            if self.solMatrix[first][second] != 0 and self.exMatrix[first][second] == 0:
                strongReactions += 1
                products.append(self.effects[self.solMatrix[first][second] - 1])
                if self.effects[self.solMatrix[first][second] - 1] in self.optionalEffects:
                    self.exMatrix[first][second] = 1

        wincount = 0

        #2. store to buffer
        if weakReactions > 0:
            textbuffer += "There were: " + str(weakReactions) + " weak reactions.\n"
        if strongReactions > 0:
            textbuffer += "There were: " + str(strongReactions) + " strong reactions.\n"
            self.rng.shuffle(products)
            for p in products:
                if "Essence" in p:
                    wincount += 1
                textbuffer = self.strongRactionResulttoBuffer(p,textbuffer)
        if exhaustedReactions > 0:
            textbuffer += "There were: " + str(exhaustedReactions) + " Exhausted Reactions.\n"
            self.rng.shuffle(nonProducts)
            for p in nonProducts:
                textbuffer = self.strongRactionResulttoBuffer(p, textbuffer)
        if weakReactions == 0 and strongReactions == 0 and exhaustedReactions == 0:
            textbuffer += "There were no reactions.\n"
        if wincount == 3:
            self.textColour = '#ffbb00'
            textbuffer += "You have synthesised the philosopher's stone!"
            self.won = True

        textbuffer +="\n"
        self.resultHistory.append(textbuffer)

    def getLastRecipe(self):
        return self.recipeHistory[-1]

    def getLastResult(self):
        return self.resultHistory[-1]

    def getRecipeHistory(self):
        return self.recipeHistory

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


    def getTextColour(self):
        return self.textColour

    def getGameOver(self):
        return self.won









