__author__ = "B.Delinchant / G2ELab"

# Using AUTOGRAD : Don't use
#     Assignment to arrays A[0,0] = x
#     Implicit casting of lists to arrays A = np.sum([x, y]), use A = np.sum(np.array([x, y])) instead.
#     A.dot(B) notation (use np.dot(A, B) instead)
#     In-place operations (such as a += b, use a = a + b instead)
#     Some isinstance checks, like isinstance(x, np.ndarray) or isinstance(x, tuple), without first doing from autograd.builtins import isinstance, tuple.

import autograd.numpy as np
import math
def ackley(x,y):
    fobj = -20 * np.exp(-0.2 * np.sqrt(0.5 * (np.square(x) +np.square(y)))) - np.exp(0.5 * (np.cos(2 * math.pi * x) + np.cos(2 * math.pi * y))) + math.exp(1) + 20
    return locals().items()

#Plot
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt
from matplotlib import cm
#from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

fig = plt.figure()
ax = plt.axes(projection="3d")

X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
res = ackley(X,Y)
dico = {k: v for k, v in res.__iter__()}  # conversion en dictionnaire
Z = dico['fobj']

surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)


plt.show()


#Optimize
from noload.optimization.optimProblem import Spec, OptimProblem
#This function is non derivable in [0,0] that can lead to convergence issue.
#Initial guess must be different from [0,0]
spec = Spec(variables=['x', 'y'], bounds=[[-5, 5], [-5, 5]], objectives=['fobj'], xinit = [2,2])
optim = OptimProblem(model=ackley, specifications=spec)
result = optim.run()

result.printResults()
result.plotResults()
