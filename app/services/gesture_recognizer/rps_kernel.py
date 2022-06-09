import random

winEas = loseEas = tieEas = winInt = loseInt = tieInt = winHard = loseHard = tieHard = winExp = loseExp = tieExp = \
    winspec = losespec = tiespec = 0.0

hiddenfound = False

buildTMatrix = {'rr': 1, 'rp': 1, 'rs': 1, 'pr': 1, 'pp': 1, 'ps': 1, 'sr': 1, 'sp': 1, 'ss': 1}
buildTMatrixL = {'rr': 1, 'rp': 1, 'rs': 1, 'pr': 1, 'pp': 1, 'ps': 1, 'sr': 1, 'sp': 1, 'ss': 1}
buildTMatrixT = {'rr': 1, 'rp': 1, 'rs': 1, 'pr': 1, 'pp': 1, 'ps': 1, 'sr': 1, 'sp': 1, 'ss': 1}

n = 3
m = 3
tMatrix = [[0] * m for i in range(n)]
tMatrixL = [[0] * m for i in range(n)]
tMatrixT = [[0] * m for i in range(n)]

probabilitiesRPS = [1 / 3, 1 / 3, 1 / 3]

def checkStats(wlt, modeChosen):
    global winEas
    global loseEas
    global tieEas
    global winInt
    global loseInt
    global tieInt
    global winHard
    global loseHard
    global tieHard
    global winExp
    global loseExp
    global tieExp
    global winspec
    global losespec
    global tiespec

    if (modeChosen == 1):
        if (wlt == 0):
            winEas += 1
        elif (wlt == 1):
            loseEas += 1
        else:
            tieEas += 1
    elif (modeChosen == 2):
        if (wlt == 0):
            winInt += 1
        elif (wlt == 1):
            loseInt += 1
        else:
            tieInt += 1
    elif (modeChosen == 3):
        if (wlt == 0):
            winExp += 1
        elif (wlt == 1):
            loseExp += 1
        else:
            tieExp += 1
    elif (modeChosen == 4):
        if (wlt == 0):
            winHard += 1
        elif (wlt == 1):
            loseHard += 1
        else:
            tieHard += 1
    else:
        if (wlt == 0):
            winspec += 1
        elif (wlt == 1):
            losespec += 1
        else:
            tiespec += 1


def buildTransitionProbabilities(pC, c, winloss):
    global buildTMatrix
    global buildTMatrixL
    global buildTMatrixT
    choi = ['r', 'p', 's']

    if winloss == "Win!":
        for i, x in buildTMatrix.items():
            if ('%s%s' % (choi[pC], choi[c]) == i):
                buildTMatrix['%s%s' % (choi[pC], choi[c])] += 1
    elif winloss == "Tied!":
        for i, x in buildTMatrixT.items():
            if ('%s%s' % (choi[pC], choi[c]) == i):
                buildTMatrixT['%s%s' % (choi[pC], choi[c])] += 1
    else:
        for i, x in buildTMatrixL.items():
            if ('%s%s' % (choi[pC], choi[c]) == i):
                buildTMatrixL['%s%s' % (choi[pC], choi[c])] += 1

    return buildTransitionMatrix(winloss)


def buildTransitionMatrix(winlosstwo):
    global tMatrix
    global tMatrixL
    global tMatrixT

    if winlosstwo == "Win!":
        rock = buildTMatrix['rr'] + buildTMatrix['rs'] + buildTMatrix['rp']
        paper = buildTMatrix['pr'] + buildTMatrix['ps'] + buildTMatrix['pp']
        scissors = buildTMatrix['sr'] + buildTMatrix['ss'] + buildTMatrix['sp']
        choi = ['r', 'p', 's']
        for row_index, row in enumerate(tMatrix):
            for col_index, item in enumerate(row):
                a = int(buildTMatrix['%s%s' % (choi[row_index], choi[col_index])])
                if (row_index == 0):
                    c = a / rock
                elif (row_index == 1):
                    c = a / paper
                else:
                    c = a / scissors
                row[col_index] = float(c)
        return (tMatrix)
    elif winlosstwo == "Tied!":
        rock = buildTMatrixT['rr'] + buildTMatrixT['rs'] + buildTMatrixT['rp']
        paper = buildTMatrixT['pr'] + buildTMatrixT['ps'] + buildTMatrixT['pp']
        scissors = buildTMatrixT['sr'] + buildTMatrixT['ss'] + buildTMatrixT['sp']
        choi = ['r', 'p', 's']
        for row_index, row in enumerate(tMatrixT):
            for col_index, item in enumerate(row):
                a = int(buildTMatrixT['%s%s' % (choi[row_index], choi[col_index])])
                if (row_index == 0):
                    c = a / rock
                elif (row_index == 1):
                    c = a / paper
                else:
                    c = a / scissors
                row[col_index] = float(c)
        return (tMatrixT)

    else:
        rock = buildTMatrixL['rr'] + buildTMatrixL['rs'] + buildTMatrixL['rp']
        paper = buildTMatrixL['pr'] + buildTMatrixL['ps'] + buildTMatrixL['pp']
        scissors = buildTMatrixL['sr'] + buildTMatrixL['ss'] + buildTMatrixL['sp']
        choi = ['r', 'p', 's']
        for row_index, row in enumerate(tMatrixL):
            for col_index, item in enumerate(row):
                a = int(buildTMatrixL['%s%s' % (choi[row_index], choi[col_index])])
                if (row_index == 0):
                    c = a / rock
                elif (row_index == 1):
                    c = a / paper
                else:
                    c = a / scissors
                row[col_index] = float(c)
        return (tMatrixL)


def checkWin(user, machine, mode):
    win = False
    tie = False
    if (mode == 73):
        if (user == 0):
            if (machine == 2 or machine == 3):
                win = True
                tie = False
            elif (machine == 1 or machine == 4):
                win = False
                tie = False
            elif (machine == 0):
                tie = True
            else:
                print("Something wierd happened and machine was: %s" % machine)
        elif (user == 1):
            if (machine == 0 or machine == 4):
                win = True
                tie = False
            elif (machine == 2 or machine == 3):
                win = False
                tie = False
            elif (machine == 1):
                tie = True
            else:
                print("Something wierd happened and machine was: %s" % machine)
        elif (user == 2):
            if (machine == 1 or machine == 3):
                win = True
                tie = False
            elif (machine == 0 or machine == 4):
                win = False
                tie = False
            elif (machine == 2):
                tie = True
            else:
                print("Something wierd happened and machine was: %s" % machine)
        elif (user == 3):
            if (machine == 4 or machine == 1):
                win = True
                tie = False
            elif (machine == 2 or machine == 0):
                win = False
                tie = False
            elif (machine == 3):
                tie = True
            else:
                print("Something wierd happened and machine was: %s" % machine)
        else:
            if (machine == 2 or machine == 0):
                win = True
                tie = False
            elif (machine == 1 or machine == 3):
                win = False
                tie = False
            elif (machine == 4):
                tie = True
            else:
                print("Something wierd happened and machine was: %s" % machine)
    else:
        if (user == 0):
            if (machine == 2):
                win = True
                tie = False
            elif (machine == 1):
                win = False
                tie = False
            elif (machine == 0):
                tie = True
            else:
                print("Something wierd happened and machine was: %s" % machine)
        elif (user == 1):
            if (machine == 0):
                win = True
                tie = False
            elif (machine == 2):
                win = False
                tie = False
            elif (machine == 1):
                tie = True
            else:
                print("Something wierd happened and machine was: %s" % machine)
        else:
            if (machine == 1):
                win = True
                tie = False
            elif (machine == 0):
                win = False
                tie = False
            elif (machine == 2):
                tie = True
            else:
                print("Something wierd happened and machine was: %s" % machine)

    if (tie == True):
        checkStats(2, mode)
        return "Tied!"
    elif (win):
        checkStats(0, mode)
        return "Win!"
    else:
        checkStats(1, mode)
        return "Lose!"


def expertMode(user_move):
    global probabilitiesRPS
    choices = ["rock", "paper", "scissors"]
    choi = ['r', 'p', 's']
    continuePlaying = True
    prevChoice = ""
    choice = 3
    probRock = 0
    probPaper = 0
    probScissors = 0
    choice = user_move

    machineChoice = random.randint(0, 2)
    result = checkWin(choice, machineChoice, 3)

    prevChoice = choice

    transMatrix = buildTransitionProbabilities(prevChoice, choice, result)
    machineChoice = random.randint(1, 100)
    probabilitiesRPS[0] = transMatrix[prevChoice][0]
    probabilitiesRPS[1] = transMatrix[prevChoice][1]
    probabilitiesRPS[2] = transMatrix[prevChoice][2]
    rangeR = probabilitiesRPS[0] * 100
    rangeP = probabilitiesRPS[1] * 100 + rangeR
    if (machineChoice <= rangeR):
        machineChoice = 1
    elif (machineChoice <= rangeP):
        machineChoice = 2
    else:
        machineChoice = 0

    result = checkWin(choice, machineChoice, 3)
    prevChoice = choice
    print("You chose %s" % choices[choice])
    print("The machine chose %s" % choices[machineChoice])
    print("You %s" % result)
    return choices[machineChoice]