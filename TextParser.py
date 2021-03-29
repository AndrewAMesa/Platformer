


class TextParser():

    def parseText(self, levelNum):
        self.count = 0
        file = open("Levels/Level" + str(levelNum) + ".txt")
        line = file.readline()
        tempX = 0
        for x in range(0, len(line)):
            if line[x] == "i":
                self.startingSpotX = tempX
                self.startingSpotY = self.count
                self.BOARDWIDTH += 1
                tempX += 1
                self.lineList.append(line[x])
            elif line[x] != ',' and line[x] != '\n':
                self.BOARDWIDTH += 1
                tempX += 1
                self.lineList.append(line[x])
        self.count += 1
        while line:
            line = file.readline()
            tempX = 0
            for x in range(0, len(line)):
                if line[x] == "i":
                    self.startingSpotX = tempX
                    self.startingSpotY = self.count
                    tempX += 1
                    self.lineList.append(line[x])
                elif line[x] != "," and line[x] != "\n":
                    tempX += 1
                    self.lineList.append(line[x])
            self.count += 1
        self.count -= 1