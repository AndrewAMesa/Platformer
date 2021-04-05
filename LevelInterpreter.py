import pygame

class LevelInterpreter:

    def parseText(self, levelNum):
        self.count = 0
        file = open("Levels/Level" + str(levelNum) + ".txt")
        line = file.readline()
        for x in range(0, len(line)):
            if line[x] == "i":
                self.startingSpotX = x
                self.startingSpotY = self.count
                self.BOARDWIDTH += 1
                self.lineList.append(line[x])
            elif line[x] != ',' and line[x] != '\n':
                self.BOARDWIDTH += 1
                self.lineList.append(line[x])
        self.count += 1
        while line:
            line = file.readline()
            for x in range(0, len(line)):
                if line[x] == "i":
                    self.startingSpotX = x
                    self.startingSpotY = self.count
                    self.lineList.append(line[x])
                elif line[x] != "," and line[x] != "\n":
                    self.lineList.append(line[x])
            self.count += 1
        self.count -= 1

    def convert(self):
        tempZ = 0
        tempTop = 0 - self.TILESIZE
        self.tileList2 = [[0] * (self.BOARDWIDTH) for x in range(self.count)]

        for y in range(self.count):
            tempTop += self.TILESIZE
            tempLeft = 0 - self.TILESIZE
            for x in range(self.BOARDWIDTH):
                tempLeft += self.TILESIZE
                #if self.lineList[tempZ] == "w":
