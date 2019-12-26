################################
import numpy as np
import matplotlib.pyplot as plt
import cmath
from scipy.optimize import fsolve

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
#preamble
#################################
wl = 300e-9

z_r = 5
#parameters
################################
k = 2*np.pi/wl
w_0 = np.sqrt(wl*z_r/np.pi)

@np.vectorize
def q(z):
    return complex(z,z_r)

@np.vectorize
def R(z):
    return z/(z**2 + z_r**2)

@np.vectorize
def w(z):
    return w_0 * np.sqrt(1+(z/z_r)**2)

@np.vectorize
def alpha(z):
    return np.arctan((z)/z_r)

z = np.linspace(-50,50,100)

plt.plot(z,w(z)/w_0)
plt.plot(z,-w(z)/w_0)
plt.show()

plt.plot(z,R(z))
plt.show()

plt.plot(z,alpha(z))
plt.show()

phase = k*np.linspace(0,10,5)


fig = plt.figure()
ax = fig.gca(projection = '3d')

@np.vectorize
def Rho(z,phase):
    return (phase - k*z + np.arctan(z/z_r))*2*(z**2 + z_r**2)/z

z = np.linspace(0,z_r,100)
t = np.linspace(0,2*np.pi,100)

zz,tt = np.meshgrid(z,t)

rr = Rho(zz,0)

xx = rr * np.cos(tt)
yy = rr * np.sin(tt)
zz
print(xx)
print(zz)

surf = ax.plot_surface(xx, yy, zz, cmap=cm.coolwarm,
                   linewidth=1, antialiased=False)
#fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
