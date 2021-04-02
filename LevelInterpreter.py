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
                if self.lineList[tempZ] == "w":
                    tempCheck = int((random.random() * 6)) + 1
                    if tempCheck == 1:
                        tempWall = self.Wall
                    elif tempCheck == 2:
                        tempWall = self.Wall2
                    elif tempCheck == 3:
                        tempWall = self.Wall3
                    elif tempCheck == 4:
                        tempWall = self.Wall4
                    elif tempCheck == 5:
                        tempWall = self.Wall5
                    elif tempCheck == 6:
                        tempWall = self.Wall5
                    self.tileList2[y][x] = tile(self.TILESIZE, tempLeft, tempTop, pygame.image.load(tempWall))
                    self.tileList2[y][x].isWall = True
                    tempZ += 1