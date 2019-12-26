"""
This code uses the angular spectrum method for optics. This means that it
takes a fourier decomposition of the given signal in the xy plane, propagates
through the system via the ASM, and the take the inverse fourier transform. 

"""

#################################################################################
#preamble
import numpy as np
from scipy import signal
import cmath
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
fig = plt.figure()
ax = fig.gca(projection='3d')
################################################################################
#parameters
def init_sig(x,y):
    return np.exp(-np.sqrt(x**2 + y**2))

@np.vectorize
def cexp(x):
    return np.exp(complex(0,x))

def prop_factor(k_x,k_y,k,z):
    return cexp(np.sqrt(k**2 - k_x**2 - k_y**2)*z)

x_lim = 10
y_lim = 10
npoints = 100

k = 1
dt = 1
dz = 1

def ap_1(x,y):
    return np.cos(x) - np.sin(y)


aperature_array = [ap_1]

################################################################################
#OPTICAL CIRCUIT
el_dict = {'-':1,'_':2}
#specifies refractive index of free propagation

op_circuit = '______------|0|------_______'

#each dash corresponds to a unit free propagation, each | encloses aperatures
#which are labelled as the index of the aperature array
################################################################################
#decompose initial signal into its fourier components

x_sample = np.linspace(0,x_lim,npoints)
y_sample = np.linspace(0,y_lim,npoints)

xx,yy = np.meshgrid(x_sample,y_sample)
#set the real space domain the code works over

dk_x_grid = 2*np.pi/x_lim
dk_y_grid = 2*np.pi/y_lim 
kxkx,kyky = np.meshgrid(np.arange(0,npoints)*dk_x_grid,np.arange(0,npoints)*dk_y_grid)
print(kxkx.shape)
#k grid

aperature_array_k = [np.fft.fft2(j(xx,yy)) for j in aperature_array]

init_sig_r = init_sig(xx,yy)
init_sig_k = np.fft.fft2(init_sig(xx,yy))

def CircuitInterpreter(start = 0):
    #circuit element generator. returns propagator
    for i in range(start,len(op_circuit)):
        if op_circuit[i].isdigit():
            yield [aperature_array_k[int(op_circuit[i])],'a']
        elif op_circuit[i] == '|':
            continue
        else:
            yield [lambda kx,ky: prop_factor(kx,ky,k*el_dict[op_circuit[i]],dz),'p']
            #will throw error if not in dict

#main loop through circuit
sig = init_sig_r
sig_k = init_sig_k
sig_array = [init_sig_r]
ci = CircuitInterpreter()
for j in range(0,len(op_circuit)):
    try:
        [prop,t] = ci.__next__()
    except StopIteration:
        break
    if t == 'p':
        prop_num = prop(kxkx,kyky)
        sig_k = sig_k*prop_num
    elif t == 'a':
        sig_k = 2*np.pi*signal.convolve2d(sig_k,prop,mode='same')

    sig = np.fft.ifft2(sig_k)
    print(sig)
    sig_array.append(sig)
    ax.plot_surface(xx,yy,sig.real)
    plt.show()
    exit()
    #for some reason I lose a lot of information with the fft's. 
    #This needs to be looked into further, perhaps I have not created
    #my reciprocal grid up correctly? 
