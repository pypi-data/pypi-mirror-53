import autograd.numpy as np

'''Define optimization specification including objectives and constraints'''
class Spec:
    iNames      = []  #noms des variables d'optimisation
    bounds      = []  #domaine de recherche
    xinit       = []  #valeurs initiales
    objectives  = []  #noms des objectifs
    eq_cstr     = []  #noms des contraintes d'équalité
    eq_cstr_val = []  #valeurs des contraintes d'égalité
    ineq_cstr   = []  #noms des contraintes d'inégalité
    ineq_cstr_bnd = []  # domaine des contraintes d'inégalité
    freeOutputs = []  # list of outputs to monitor
    nb          = 0
    oNames       = []
    def __init__(self, variables, bounds, objectives, eq_cstr=[], eq_cstr_val=[], ineq_cstr=[], ineq_cstr_bnd=[], freeOutputs=[], xinit=[]):
        self.iNames = variables
        self.bounds = bounds
        self.xinit = xinit
        self.objectives = objectives
        self.eq_cstr = eq_cstr
        self.eq_cstr_val = eq_cstr_val
        self.ineq_cstr = ineq_cstr
        self.ineq_cstr_bnd = ineq_cstr_bnd
        self.freeOutputs = freeOutputs
        self.computeAttributes()

    def computeAttributes(self):
        self.oNames = np.concatenate((self.objectives, self.eq_cstr, self.ineq_cstr, self.freeOutputs), axis=0)
        self.nb = len(self.oNames)

    def removeObjective(self, fobj):
        self.objectives.remove(fobj)
        self.computeAttributes()

    def insertObjective(self, position, fobj):
        self.objectives.insert(position, fobj)
        self.computeAttributes()

    def appendConstraint(self, cstr, value):
        self.eq_cstr.append(cstr)
        self.eq_cstr_val.append(value)
        self.computeAttributes()

    def removeLastEqConstraint(self):
        self.eq_cstr.pop()
        self.eq_cstr_val.pop()
        self.computeAttributes()


