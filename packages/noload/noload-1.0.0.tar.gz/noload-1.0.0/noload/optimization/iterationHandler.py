from typing import List

class Solution:
    iData = []
    oData = []

    def __init__(self, inp, out):
        self.iData = inp
        self.oData = out


class Iterations:
    solutions: Solution = []
    iNames = []
    oNames = []

    def __init__(self, iNames, oNames, handler = None):
        self.iNames = iNames
        self.oNames = oNames
        self.solutions = []
        self.handler = handler #TODO : n'est plus utilisé. Modifier la création automatique du Handler (dans constructeur Wrapper) lorsqu'il s'agit d'un affichage dynamique : dynamicPlot.update

    def updateData(self, inp, out):
        self.solutions.append(Solution(inp.copy(), out.copy()))
        if (self.handler):
            self.handler(self.solutions)

    def print(self):
        print([sol.iData for sol in self.solutions])
        print([sol.oData for sol in self.solutions])

    def plotXY(self):
        import noload.gui.plotIterations as pi
        pi.plotXY(self)
    def plotIO(self):
        import noload.gui.plotIterations as pi
        pi.plotIO(self)


def printHandler(sols:List[Solution]):
    sols
    print(sols[-1].iData)
    print(sols[-1].oData)

