# Python Client to Connect Solve-Hub xtellix Optimization Server
## Draft Version 0.0.1
This is a simple example usage of how to initialize the Optimization Engine Server and Perform Optimization on your objective functions. *The remaining documents is in two (2) parts: **Section A: Initializing Server**; and  **Section B: Running the Optimization Loop**.*

# SECTION A
## PREREQUISITES: INSTALL KEY LIBRARIES & INITIALIZE SERVER
**Install xtellixClient using pip command [https://pypi.org/project/xtellixClient/](https://pypi.org/project/xtellixClient-0.0.1/)**
Read more at [Github](https://github.com/markamo/xtellixClient)
```
pip install xtellixClient
```

### STEP 1A: IMPORT XTELLIX CLIENT LIBRARIES
Import the xtellixClient module
```python
import xtellixClient.xtellixClient as xm
```

### STEP 1B: IMPORT OTHER KEY LIBRARIES
```python
import math
import numpy as np
from tqdm import trange
import time
```

### STEP 2: OBJECTIVE FUNCTION
**Define your cost or objective function**
Here we define the Griewank function as en example. More infomation about the Griewank benchmark function can be found on the [web](https://www.sfu.ca/~ssurjano/griewank.html). 

```python
def griewank_function(x, dim):
    """Griewank's function 	multimodal, symmetric, inseparable """
    sumPart = 0
    prodPart = 1
    for i in range(dim):
        sumPart += x[i]**2
        prodPart *= math.cos(float(x[i]) / math.sqrt(i+1))
    return 1 + (float(sumPart)/4000.0) - float(prodPart)  
```

### OPTIONAL STEP 2B: COST FUNCTION WRAPPERS FOR THE OBJECTIVE FUNCTION
To make it easier to dynamically call other benchmark functions without changing much of the code, we recommend defining a general purpose wrapper to be called during the optimization process 

```python
def cost_function(newSuggestions, dim):
    """Generic function wrapper for the cost function """
    return griewank_function(newSuggestions, dim)
```

### STEP 3: INITIALIZE CONNECTION TO THE OPTIMIZATION SERVER
Connect to your unique optimization server using your provided credentials: **server_endpoint**, and **client_secret_token**. These are two are used to established a secured successful connection before you can begin any optimization project. Watch for server connection errors and contact the support team for assistance

```python
#set server_endpoint and client_secret_token as variables
sever_endpoint = "http://127.0.0.1:5057"
client_secret = 1234567890

#Initialize connection and watch for errors
xm.connect(sever_endpoint, client_secret)
```

### STEP 4: INITIALIZE THE OPTIMIZATION ENGINE
Let's begin by setting up all the initial parameters for the objective function, then the optimization engine

**a. Initial parameters for the Cost Function**
```python
ubound=600  #upper bound of the Griewank function
lbound=-600 #lower bound of the Griewank function
dim=100      #problem dimension

```

**b. Optimization Engine Settings**
```python
initMetric = 30000000 #largest possible cost function value - arbitrary very large/low number for minimization/maximization problems respectively
maxIter=dim*200 # maximum number of iterations. We recommend 100 to 200 times the dimension of the problem. and 10 - 50 times for intensive CPU problems
maxSamples=8 # maximum number of default stochastic sampling
iseedId=0 #Seed value for random number generator
minOrMax = True  ### True for MINIMIZATION | False for MAXIMIZATION
```

**c. Prepare the initial parameter value**
```python
x0 = np.ones([dim]) * lbound 
```
**d. Compute the first objective function**
```python
fobj = cost_function(x0, dim)
initMetric = fobj #Optional: use the first value as initial metric
print("Initial Objective Function Value = ",fobj)
```

**e. Initialize Optimization Engine**
```python
xm.initializeOptimizer(initMetric,ubound, lbound, dim, maxIter, maxSamples, x0, iseedId,minOrMax)
```


# SECTION B 
## THE OPTIMIZATION LOOP: SOLVING YOUR OPTIMIZATION PROBLEM
### 3 SIMPLE STEPS: GET -> COMPUTE -> UPDATE
Solving the optimizatin problem (here: Griewank function) is done in the following three (3) steps: 
**a. Get new suggested parameters from the optimization server**
```python
newSuggestions = xm.getParameters()

```
**b. Compute new cost function based on the new parameters**
```python
fobj = cost_function(newSuggestions, dim)
```

**c. Send new cost function value to the optimization server**
```python
xm.updateObjectiveFunctionValue(fobj)
```

**d. Repeat the whole process until optimization is achieved**
The whole process can be summarized below: 

#### The Optimization Loop with comments
```python

#OPtional Step: Use TQDM Library for nice progress bar 
with trange(maxIter) as t:
    for i in t:
        ##a: Get parameters from Optimization Engine
        newSuggestions = xm.getParameters()
        
        ##b: Compute new cost function value based on the parameters
        fobj = cost_function(newSuggestions, dim)
        
        ##c: Send new cost function value to optimization server
        xm.updateObjectiveFunctionValue(fobj)

        ##Optional step: Check the progress of the optmization
        obj,pareato,_,svrit = xm.getProgress()        

        ###Optional step: Update the progress bar
        t.set_description('Function Eval %i' % i)
        t.set_postfix(current=obj, best=pareato)

```

#### The Optimization Loop WITHOUT comments
We see the simplicity of the process without the comments
```python
for i in range(maxIter):
    newSuggestions = xm.getParameters()        
    fobj = cost_function(newSuggestions, dim)        
    xm.updateObjectiveFunctionValue(fobj)
```

### GET FINAL PARAMETERS FROM SERVER
*Get the optimized parameters*
```python
x0 = xm.getParameters()

```
*Or Get the optimized parameter (force download a fresh copy from the server)*
```python
x0 = xm.getParameters(False)

```

*Calculate the final objective function value*
```python
fobj = cost_function(x0, dim)
```
*Print final objective function value and optimized parameters*
```python
print(fobj)
print(x0)
```

## The full code for the above example
```python
import xtellixClient.xtellixClient as xm
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

```
