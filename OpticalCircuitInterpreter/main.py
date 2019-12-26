"""
This program is designed to allow the user to define an optical circuit, and 
calculate how the system propagates using ray matrices. 
"""
#Author: James Bate
################################################################################
import numpy as np
import cmath
#preamble
################################################################################
k = 1 #relavent if I want to extend to proper units, such that results can be tested against experiment 
q_init = complex(1,1)


L0 = np.array([[1,0],[-0.5,1]])
L1 = np.array([[1,0],[-0.25,1]])
M0 = np.array([[],[]])

free_prop = np.array([[1,2],[0,1]])
lens_list = [L0,L1]
mirror_list = [M0]
#Prepare all relavent matrices. free_prop, lens_list and mirror_list are essential 
#In this list, the second number must correspond to its index
#parameters
################################################################################
#circuit diagram



op_circuit = '--|L0|----|L1|--'



#- -> free prop
#|| enclose elements
#ML mirror and lens resp.
#number corresponds to index in list given above

#The available elements can be arbitrarily extended. Just make sure to add
#to the el_dict so the iterator can interpret what the letters stand for

################################################################################


class CircuitInterpreter:

    #constructor
    def __init__(self,start):
        self.nloop = start
        self.iter_flag = False


    def __iter__(self):
        return self


    def Interpreter(self,el):
        #returns matrix element to use, or array of them
        el_dict = {
            '-': free_prop,
            'M': mirror_list,
            'L': lens_list
        }
        if self.iter_flag == True:
            if self.el.isnumeric():
                return self.arr[int(el)]
            #Here I assume that the second number of the 
            #element corresponds to its index
        if el == '|':
            if self.iter_flag == True:
                self.iter_flag = False
            else:
                pass
        elif el.isalpha():
            self.arr = el_dict[el]
            self.iter_flag = True
        elif el == '-':
            return free_prop
        else:
            print('Unrecognised Character')
            exit()



    def it_func(self):
        if self.nloop < len(op_circuit):
            self.el = op_circuit[self.nloop]
            self.nloop += 1    
            return self.Interpreter(self.el)
        else:
            raise StopIteration()    

    def __next__(self):
        x = self.it_func()
        while x is None:
            x = self.it_func()
        return x

class Circuit():
    def __init__(self):
        pass

    def Calculate_Matrix(self,start, end):
        self.CI = CircuitInterpreter(start)
        self.System_Matrix = next(self.CI)
        for i in range(start,end):
            try:
                self.System_Matrix = self.System_Matrix.dot(next(self.CI))
            except StopIteration:
                break  
        return self.System_Matrix

    def Calculate_q_final(self,start,end,q_init):
        M = self.Calculate_Matrix(start,end)
        return M.dot(q_init)



#Example calculations

C = Circuit()
System_Matrix = C.Calculate_Matrix(0,len(op_circuit))
print(System_Matrix)

q_final = C.Calculate_q_final(0,len(op_circuit),q_init)
print(q_final)



