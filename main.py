import game

sd = input("Input game seed:\n")
pn = input("Player Number:\n")
dif = input("Input Difficulty:\n")

newGame = game.game(sd,pn,dif)

gameover = False
while not newGame.won or not gameover:
    mystring = input("Input recipy to mix:\n")

    if mystring == "quit":
        print(newGame.getSolution())
        gameover=True
        break
    else:
        newGame.mix(mystring)
        print(newGame.getLastResult())

