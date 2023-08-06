__author__ = "B.Delinchant / G2ELab"

# Using AUTOGRAD : Don't use
#     Assignment to arrays A[0,0] = x
#     Implicit casting of lists to arrays A = np.sum([x, y]), use A = np.sum(np.array([x, y])) instead.
#     A.dot(B) notation (use np.dot(A, B) instead)
#     In-place operations (such as a += b, use a = a + b instead)
#     Some isinstance checks, like isinstance(x, np.ndarray) or isinstance(x, tuple), without first doing from autograd.builtins import isinstance, tuple.

import autograd.numpy as np
def simionescu(x, y, rr, rs, n):
    fobj = 0.1 * x * y
    ctr = x * x + y * y - np.power(rr + rs * np.cos(n * np.arctan(x / y)), 2)
    return locals().items()

#Plot
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

fig = plt.figure()
ax = plt.axes(projection="3d")

X = np.arange(-1.25, 1.25, 0.1)
Y = np.arange(-1.25, 1.25, 0.1)
X, Y = np.meshgrid(X, Y)
res = simionescu(X,Y,1,0.2,8)
dico = {k: v for k, v in res.__iter__()}  # conversion en dictionnaire
Z = dico['fobj']

surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)


# plt.show()


#Optimize
from noload.optimization.optimProblem import Spec, OptimProblem
#This function is non defined in [0,0], initial guess must be different from [0,0]
spec = Spec(variables=['x', 'y'], bounds=[[-1.25, 1.25], [-1.25, 1.25]], objectives=['fobj'], xinit = [0,1],
            ineq_cstr=['ctr'], ineq_cstr_bnd=[[None, 0]], #inequality constraints
            )
optim = OptimProblem(model=simionescu, specifications=spec, parameters={'rr':1, 'rs':0.2, 'n':8})
result = optim.run()

result.printResults()
result.plotResults()
