# -*- coding: utf-8 -*-
"""
Created December 2019
@author: James Bate
"""
################################################################################
import numpy as np
from scipy.integrate import odeint,quad
import matplotlib.pyplot as plt
#preamble
################################################################################
#Please Note:
#The y axis is given in terms of N_th of the final section.
#be aware of the resolution on the t axis. If it's too low,
#you can get some very unexpected results
def R_2(t):
    return 0.8
def R_2_f(t):
    return 0

params1 =   {
                'L_c':1e-1,
                'mR_1':0.95,
                'mR_2':0.95,
                'V':1e-5,
                'R_2': R_2,
                'tau_2': 90,
                'omega_1':1e15,
                'N_i/N_th':0,
                'n_0': 0.01,
                'n_index':1,
                'tau_c':0.1,

            }
params2 =   {
                'L_c':1e-1,
                'mR_1':0.95,
                'mR_2':0.95,
                'V':1e-5,
                'R_2': R_2,
                'tau_2':90,
                'omega_1':1e15,
                'n_index':1,
                'tau_c':0.5,
            }
PropagationTimeline =   [
                            [params1,0,500],
                            [params2,500,600],
                        ]

#parameters
################################################################################
class Cavity:
    def __init__(self,L_c,R_1,R_2,V):
        self.L_c = L_c
        self.R_1 = R_1
        self.R_2 = R_2
        self.V = V
        self.ComponentType = 'Cavity'
    def Elongate(self,dL):
        self.L_c = self.L_c + dL


class LaserCavitySystem(Cavity):
    def __init__(self,custom_params = {}):
        self._Components = {}
        self.nComponents = 0
        self.DefaultCavityName = 'Cavity'

        #parameter keys
        self.keylist = set(['L_c','mR_1','mR_2','V','R_2','n_index','omega_1','tau_2','tau_c'])
        self.custom_params = custom_params

        #If custom params not empty, load them. else, use default params
        self.GetParams()

        #add cavity
        super().__init__(self.L_c,self.mR_1,self.mR_2,self.V)
        self._Components.update({self.DefaultCavityName:Cavity(self.L_c,self.R_1,self.R_2,self.V)})
        #Done this way since system must have one and only one cavity
        self.nComponents += 1
        self.values = []

        self.timesteps = 10000
        self.t_array = np.array([])

    def GetParams(self):
        self.customkeys = set(self.custom_params.keys())
        if bool(self.custom_params):
             self.GetCustomParams()
        else:
            self.GetDefaultParams()
        self.LoadParams()

    def GetDefaultParams(self):
        self.param_dict =  {
                                'L_c':1e-1,
                                'mR_1':0.95,
                                'mR_2':0.95,
                                'V':1e-5,
                                'R_2': R_2,
                                'tau_2':1,
                                'omega_1':1e15,
                                'N_i/N_th':2,
                                'n_0': 0.0001,
                                'n_index':1,
                                'tau_c':3,
                            }
        return

    def GetCustomParams(self):
        if not self.CheckCustomParams():
            print('Incorrect Parameter Set')
            exit()
        self.param_dict = self.custom_params
        return

    def UpdateParams(self,params):
        self.custom_params = params
        self.GetParams()
        return

    def CheckCustomParams(self):
        return self.keylist.issubset(self.customkeys)

    def LoadParams(self):
        self.L_c = self.param_dict['L_c']
        self.mR_1 = self.param_dict['mR_1']
        self.mR_2 = self.param_dict['mR_2']
        self.V = self.param_dict['V']
        self.R_2 = self.param_dict['R_2']
        self.tau_2 = self.param_dict['tau_2']
        self.omega_1 = self.param_dict['omega_1']
        self.n_index = self.param_dict['n_index']
        self.tau_c = self.param_dict['tau_c']

        #self.tau_c = -2*self.L_c*self.n_index/(3e8*np.log(self.mR_1*self.mR_2))
        self.N_th = (1/self.tau_c)
        if 'n_0' in self.param_dict:
            self.n_0 = self.param_dict['n_0']
        else:
            self.n_0 = self.soln[-1][1]
        if 'N_i/N_th' in self.param_dict:
            self.N_i = self.param_dict['N_i/N_th']*self.N_th
        else:
            self.N_i = self.soln[-1][0]




    def Component(self,label):
        return self._Components[label]

    #Rate Equations
    def f(self,y,t):
        f0 = self.R_2(t) - y[0]*y[1]/(self.N_th)*(1/self.tau_c) - y[0]/self.tau_2
        f1 = (y[0]/self.N_th - 1)*y[1]*(1/self.tau_c)
        return [f0,f1]

    def PropagateSystem(self,t_i,t_f):
        self.y_0 = [self.N_i,self.n_0]
        self.t = np.linspace(t_i,t_f,self.timesteps)
        self.t_array = np.concatenate((self.t_array,self.t))

        self.soln = odeint(self.f,self.y_0,self.t)
        self.values.append(self.soln)
        return self.soln

    def Plot(self):
        self.x = np.array([]).reshape(0,2)
        for i in self.values:
            i[:,0] = i[:,0]/self.N_th
            self.x = np.concatenate((self.x,i),axis=0)
        plt.xlabel('timestep')
        plt.plot(np.array([self.t_array,self.t_array]).T,self.x)
        plt.show()

################################################################################
#Program Strucure

if __name__ ==  '__main__':


    LCS = LaserCavitySystem()

    for step in PropagationTimeline:
        LCS.UpdateParams(step[0])
        LCS.PropagateSystem(step[1],step[2])

    LCS.Plot()
