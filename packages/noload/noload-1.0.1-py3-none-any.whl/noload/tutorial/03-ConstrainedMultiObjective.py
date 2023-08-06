__author__ = "B.Delinchant / G2ELab"

# Using AUTOGRAD : Don't use
#     Assignment to arrays A[0,0] = x
#     Implicit casting of lists to arrays A = np.sum([x, y]), use A = np.sum(np.array([x, y])) instead.
#     A.dot(B) notation (use np.dot(A, B) instead)
#     In-place operations (such as a += b, use a = a + b instead)
#     Some isinstance checks, like isinstance(x, np.ndarray) or isinstance(x, tuple), without first doing from autograd.builtins import isinstance, tuple.

import autograd.numpy as np
def BinhAndKorn(x, y):
    f1 = 4*x**2+4*y**2
    f2 = (x-5)**2+(y-5)**2
    g1 = (x-5)**2+y
    g2 = (x-8)**2+(y+3)**2
    return locals().items()

#Optimize
from noload.optimization.optimProblem import Spec, OptimProblem
spec = Spec(variables=['x', 'y'], bounds=[[0, 5], [0, 3]], objectives=['f1','f2'], xinit = [0,0],
            ineq_cstr=['g1','g2'], ineq_cstr_bnd=[[None, 25],[77, None]], #inequality constraints
            )
optim = OptimProblem(model=BinhAndKorn, specifications=spec)
result = optim.run()

result.printResults()
import noload.gui.plotPareto as pp
#TODO intégrer ça dans le wrapper
# pp.AnnotedPareto([result.resultsHandler], ['f1', 'f2'], ['Pareto']) #affichage dynamique si il y a trop de points
pp.plot([result.resultsHandler], ['f1', 'f2'], ['Pareto']) #affichage statique (1 sur 2)

