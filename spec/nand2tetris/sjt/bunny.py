import os
import sys

class Writer:
    def __init__(self, FileToWrite):
        self.f = open(FileToWrite, 'w')

    def writeAndClose(self, bunnies):
        self.f.write(f"{bunnies}")
        self.f.close()

class Parser:
    def __init__(self, FileToOpen):
        # We are assuming the file exists!
        # At some point, it is worth determining
        # whether the file even exists.
        self.InFileName = FileToOpen
        self.f = open(FileToOpen, 'r')
        self.CurrLine = ''
        self.NumLines = ''
        self.InfoDict = {}
        self.bunnies = 0
        self.DEBUG = False


    def parse(self):
        for line in self.f:
            self.CurrLine = line
            self.CleanLine()
            self.advance()


    def CleanLine(self):
        line = self.CurrLine.strip() # remove line endings
        # remove comments -- split and only keep leftmost portion
        line = line.split("#")[0].strip()
        # write back data to the class variable
        self.CurrLine = line


    def advance(self):
        if self.CurrLine == "":
            return # not a valid piece of data
        else:
            #self.StoreData()
            self.countBunny()

    def countBunny(self):
        self.bunnies += self.CurrLine.lower().count("bunny")



    def write(self):
        outfile = self.InFileName.replace(".txt", ".csv")

        # now, let's sort the dictionary. This may be a bit nasty ...
        # ... after some testing, I'm just going to call a function
        self.SortDict()

        #Out text
        with open(outfile, 'w') as f:
            f.write("artist, entries, views, link\n")

            for (key, value) in self.SortedDict:
                # put tuple data into separate variables
                entries, views, link = value
                lineout = f"{key}, {entries}, {views}, {link}"
                f.write(lineout + "\n")
        # That's it, we're done!
        print("Complete.")


    def SortDict(self):
        # dictionary.items() has the format:
        # (key, (entries, total views, last link)))
        # We want to sort by Total Views which is dict.item()[1][2]
        # this gets the second entry (the tuple) and the second entry of
        #   the tuple (the total views)
        self.SortedDict = sorted(self.InfoDict.items(), key = lambda item: item[1][1], reverse=True)

def handleDirectory(dirName):
    normdirName = os.path.normpath(dirName)
    [path, name] = os.path.split(normdirName)
    srcDir = os.path.join(path, name)
    outFile = os.path.join(path, name, name + ".out")
    totBunnies = 0

    for f in os.listdir(srcDir):
        if f.endswith(".txt"):
            #print(f"processing {f}...")
            myParser = Parser( os.path.join(srcDir, f) )
            #print(f"processing {os.path.join(srcDir, f)}...")
            myParser.parse()
            #print(f"'bunny' found {myParser.bunnies} times in {f}")
            totBunnies += myParser.bunnies
    myWriter = Writer(outFile)
    myWriter.writeAndClose(totBunnies)

def handleFile(infile):
    outfile = infile.split(".txt")[0] + ".out"

    myParser = Parser(infile)
    #myParser.DEBUG = True # turn on debug flags
    myParser.parse()

    myWriter = Writer(outfile)
    myWriter.writeAndClose(myParser.bunnies)


def main():
    sourceName = sys.argv[1]
    if os.path.isdir(sourceName):
        handleDirectory(sourceName)
    else:
        handleFile(sourceName)



if __name__=="__main__":
    main()
