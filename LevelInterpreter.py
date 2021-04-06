import pygame

class LevelInterpreter:

    def readFile(self, levelNum):

        timeStr = ""
        lvlTime = -1

        a = []

        f = open("Levels/Level" + str(levelNum) + ".png", "r")

        for x in f:
            if "t" not in x:
                c = []
                for i in x:
                    if i != "\n":
                        c.append(i)

                a.append(c)

            elif "t" in x:
                timeStr = x
                timeStr = timeStr.replace("t", "")
                lvlTime = int(timeStr)

        lenX = len(a)
        lenY = len(a[0])

        b = []

        for i in range(lenY):
            d = []
            for j in range(lenX):
                d.append(0)

            b.append(d)

        lenX = len(b)
        lenY = len(b[0])

        # inverting the map
        for i in range(lenX):
            for j in range(lenY):
                b[i][j] = a[j][i]

        for i in range(lenX):
            for j in range(lenY):
                if b[i][j] == "P":
                    startingPosX = i
                    startingPosY = j
                    exit

        for i in range(lenX):
            for j in range(lenY):
                if b[i][j] == "L":
                    platform_group.add(platform1)


        return b
