from noload.optimization.wrapper import *
from noload.optimization.specifications import Spec
from noload.optimization.paretoTools import getXorYmid
from noload.optimization import optimProblem


class Solution:
    x = 0       # valeur de l'objectif 1
    y = 0       # valeur de l'objectif 2
    vars = None # valeur des variables de design
    def __init__(self, vars, x, y):
        self.x = x
        self.y = y
        self.vars = vars

    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+")"

class Pareto:
    pts  = []    #list of pt2D
    vars = []
    def __init__(self):
        self.pts = []
        self.vars = []


class EpsilonConstraint:
    w : Wrapper = None  #wrapper
    spec : Spec = None  #specifications
    fobjs    = None
    pareto: Pareto = None

    def __init__(self, wrapper):
        self.w = wrapper
        self.spec = wrapper.spec
        if (len(wrapper.spec.objectives)!=2): #TODO gérer une exception
            print("Pareto can only be applied to bi-objective specifications")
            return
        self.pareto = Pareto()
        self.fobjs = [wrapper.spec.objectives[0], wrapper.spec.objectives[1]]
        self.resultsHandler = wrapper.resultsHandler    #la sauvegarde des points de calcul sera géré par le pareto
        self.w.resultsHandler = None # à remettre à la fin

    # TODO pareto par pondération
    # def optim2D_weigthing(self, x0, optimNb=10, options=None):

        # ALGO
        # On fait varier un poid de 0 à 1 entre les 2 objectifs : f=a.f1+(1-a)f2
        # pour cela, il faut créer une nouvelle variable dans le modèle et recalculer son Jacobien df=a.df1+(1-a)df2


    def optim2D(self, x0, optimNb=5, options=None):

        #ALGO
        # init : réaliser 2 optim sur chaque objectifs avec l'autre objectif libre => utopia0
        # init : faire une sous contrainte au milieu
        # itérer : en recherchant la distance la plus grande entre 2 solutions
        #   et en fixant l'objectif dont la projection est la plus grande, au milieu de cette projection
        # convergence : nombre de point atteint

        #2 optim sans contraintes :
        #optim du premier objectif, suppression du 2ème objectif (objectif 1)

        self.modifySpec_Optim(x0, options, 1)
        xm = self.pareto.pts[0][0]
        yM = self.pareto.pts[0][1]

        #optim du 2ème objectif, suppression du 1er objectif (objectif 0)
        self.modifySpec_Optim(x0, options, 0)
        xM = self.pareto.pts[1][0]
        ym = self.pareto.pts[1][1]

        normX = xM-xm
        normY = yM-ym

        #optimisation avec l'autre objectif contraint
        x0 = self.pareto.vars[0]    # on part de la solution optimale pour fobX et on contraint sa valeur en augmentant
        x0 = self.modifySpec_Optim(x0, options, 0, (2*xm+xM)/3)   #calcul un peu à gauche du milieu (mieux que le milieu pour une courbe)

        #on reinitialise x0 à la valeur d'extremité du pareto trouvée au début.
        for i in range(1,optimNb-2):
            obj, point = getXorYmid(self.pareto.pts, normX, normY)
            x0 = self.modifySpec_Optim(x0, options, obj, point)
            print("add a point :"+ str(obj) +" / " + str(point))

        #à la fin
        self.w.resultsHandler = self.resultsHandler
        return self.pareto

    def optim2D_basic(self, x0, optimNb=10, options=None):

        #ALGO
        # init : réaliser 2 optim sur chaque objectifs avec l'autre objectif libre => utopia0
        # itérer : 2 optim sur chaque objectif avec l'autre objectif fixé entre utopia et la valeur précédente.
        # convergence : utopia n'évolue plus, ou budget en temps ou en nombre de calcul, ou en point sur le front.

        #2 optim sans contraintes :
        #optim du premier objectif, suppression du 2ème objectif (objectif 1)

        self.modifySpec_Optim(x0, options, 1)
        xm = self.pareto.pts[0][0]
        yM = self.pareto.pts[0][1]

        #optim du 2ème objectif, suppression du 1er objectif (objectif 0)
        self.modifySpec_Optim(x0, options, 0)
        xM = self.pareto.pts[1][0]
        ym = self.pareto.pts[1][1]

        #iterations d'optimisation avec l'autre objectif contraint
        #version où on connait le nombre de points sur le Pareto et on reparti sur les 2 axes
        nbpts = int((optimNb-2)/2)
        if nbpts<1:
            nbpts=1
        x0 = self.pareto.vars[1]    # on part de la solution optimale pour fobY et on contraint sa valeur en augmentant
        for i in range(1,nbpts+1):
            point = ym + i * (yM-ym)/(nbpts+1)
            # optim du premier objectif, suppression du 2ème objectif et mise en contrainte
            x0 = self.modifySpec_Optim(x0, options, 1, point)

        #on reinitialise x0 à la valeur d'extremité du pareto trouvée au début.
        x0 = self.pareto.vars[0]
        for i in range(1,nbpts+1):
            point = xm + i * (xM-xm)/(nbpts+1)
            # optim du 2ème objectif, suppression du 1ème objectif et mise en contrainte
            x0 = self.modifySpec_Optim(x0, options, 0, point)

        #à la fin
        self.w.resultsHandler = self.resultsHandler
        return self.pareto

    #for Epsilon Constraint
    def modifySpec_Optim(self, x0, options, obj, cstrVal=None):
        self.spec.removeObjective(self.fobjs[obj])
        if cstrVal!=None:
            self.spec.appendConstraint(self.fobjs[obj], cstrVal)
        result = optimProblem.SLSQP(self.w, x0, options) #1D optim
        self.spec.insertObjective(obj, self.fobjs[obj])
        if cstrVal != None:
            self.spec.removeLastEqConstraint()
        self.saveSolution(result)
        return result.x

    def saveSolution(self, result): #doit bien être appelé après avoir remis les 2 objectifs dans les spec.
        out = [self.w.rawResults[vars] for vars in self.spec.oNames]
        xopt = result.x
        self.resultsHandler.updateData(xopt, out)
        self.pareto.pts.append( [out[0], out[1]])
        self.pareto.vars.append(xopt)

