import xtellixClient as xm
import math
import numpy as np
from tqdm import trange

def griewank_function(x, dim):
    """Griewank's function 	multimodal, symmetric, inseparable """
    sumPart = 0
    prodPart = 1
    for i in range(dim):
        sumPart += x[i]**2
        prodPart *= math.cos(float(x[i]) / math.sqrt(i+1))
    return 1 + (float(sumPart)/4000.0) - float(prodPart) 

def cost_function(newSuggestions, dim):
    """Generic function wrapper for the cost function """
    return griewank_function(newSuggestions, dim)

#set server_endpoint and client_secret_token as variables
sever_endpoint = "http://127.0.0.1:5057"
client_secret = 1234567890

#Initialize connection and watch for errors
xm.connect(sever_endpoint, client_secret)

ubound=600  
lbound=-600 
dim=100
initMetric = 30000000 
maxIter=dim*200 
maxSamples=8 
iseedId=0 
minOrMax = True  ## True for MINIMIZATION | False for MAXIMIZATION

x0 = np.ones([dim]) * lbound 
fobj = cost_function(x0, dim)
print("Initial Objective Function Value = ",fobj)

xm.initializeOptimizer(initMetric,ubound, lbound, dim, maxIter, maxSamples, x0, iseedId,minOrMax)

##OPTIMIZATION LOOP
for i in range(maxIter):
    newSuggestions = xm.getParameters()        
    fobj = cost_function(newSuggestions, dim)        
    xm.updateObjectiveFunctionValue(fobj)

    ##Optional step: Check the progress of the optmization
    obj,pareato,feval,_ = xm.getProgress()   
    print("Feval = ", feval, " Best Objective = ", pareato, " Current Objective = ", obj)

x0 = xm.getParameters(False)
fobj = cost_function(x0, dim)
print(fobj)
print(x0)