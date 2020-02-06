import requests
import json

__SERVER_HOST__                 = "http://127.0.0.1:5057"
__CLIENT_SECRET__               = 1234567890
__SERVER_SECRET__               = 1234567890
__SERVER_START_API__			= "/api/start"
__SERVER_STOP_API__			    = "/api/stop"
__SERVER_PARAMETERS_API__		= "/api/parameters"
__SERVER_ALLPARAMETERS_API__	= "/api/allparameters"
__SERVER_OBJECTIVE_API__		= "/api/objective"
__SERVER_VERSION_API__		    = "/api/version"

params = []
_DIM_ = 0
rit  = 0
svr_rit = 0

current_objective = 1E300
pareato_objective = 1E300
searchMin =  True
default_headers = {'Content-Type': 'application/json'}

def version():
    """xtellix Module Copyright and Version Info """
    print( "*******************************************************")
    print("Copyright (C) 2010-2020 Dr Mark Amo-Boateng m.amoboateng@gmail.com")   
    print("Client Version: 0.0.1 beta")
    print( "*******************************************************")

def setOptimizationServerIP(address_port):
    """Set Optimization Server IP and Port Number """
    global __SERVER_HOST__
    __SERVER_HOST__ = address_port
    
def setClientSecret(secret):
    """Set Client Secret to enable Singular Access to the optimization engine """
    global __CLIENT_SECRET__
    __CLIENT_SECRET__ = secret

def connect(address_port, secret):
    """Set Server Endpoint and Client Secrets """
    setOptimizationServerIP(address_port)
    setClientSecret(secret)

    apipath = __SERVER_HOST__  + __SERVER_VERSION_API__ + "/" + str(__CLIENT_SECRET__)
    response = requests.get(apipath, verify=False, headers=default_headers)        
    r_data = json.loads(response.content)
    print( "*******************************************************")
    print("Server Version: ")    
    print( "*******************************************************")
    print(r_data)
    print( "*******************************************************")
    print("Client Version: ")
    version()

def setInitialParameters(initialSuggestions):
    """Initial parameters for optimization problem being solved"""
    global params
    params = initialSuggestions    
    sugjson = json.dumps(list(initialSuggestions))    
    apipath = __SERVER_HOST__  + __SERVER_PARAMETERS_API__ + "/" + str(__SERVER_SECRET__)
    response = requests.post(apipath, json =sugjson, headers=default_headers )

    #print(sugjson)
    #print(apipath)
    #print(response)
    
    return response


def initializeOptimizer(initMetric,ubound, lbound, dim, maxIter, maxSamples, initialSuggestions, seedId, minOrMax):
    """Default parameters for initializing the optimization engine, based on being solved"""
    global current_objective
    global pareato_objective
    global __SERVER_SECRET__ 
    global _DIM_
    global searchMin

    current_objective = initMetric
    pareato_objective = initMetric
    _DIM_ = dim
    searchMin = minOrMax

    initialize = [dim,ubound, lbound, maxIter, maxSamples, initMetric, seedId]
    iniJson = json.dumps(initialize) 
    
    apipath = __SERVER_HOST__  + __SERVER_START_API__ + "/" + str(__CLIENT_SECRET__)
    response = requests.post(apipath, json=iniJson, headers=default_headers  )
    secret = int(json.loads(response.content))

    __SERVER_SECRET__ = secret
    
    #print(apipath)
    print("New Server Secret: ", __SERVER_SECRET__)
    print("Optimization Engine Running.....")

    response1 = setInitialParameters(initialSuggestions)

    return response1
    

def getParameters(cached = True):
    """Get parameters from the Optimization Server """
    global params
    global svr_rit

    if cached == True:
        apipath = __SERVER_HOST__  + __SERVER_PARAMETERS_API__ + "/" + str(__SERVER_SECRET__)
        response = requests.get(apipath, verify=False, headers=default_headers  )
        
        r_data = json.loads(response.content)
        oldK = r_data[0]
        newK = r_data[1]
        oldPoint = r_data[2]
        newPoint = r_data[3] 
        rit = r_data[4]

        svr_rit = rit

        params[oldK] = oldPoint
        params[newK] = newPoint
    
    else:
        apipath = __SERVER_HOST__  + __SERVER_ALLPARAMETERS_API__ + "/" + str(__SERVER_SECRET__)
        response = requests.get(apipath, verify=False, headers=default_headers  )
        
        r_data = json.loads(response.content)
        
        global _DIM_
        for i in range(_DIM_):
            params[i] = r_data[i]

    #print(apipath)
    #print(response)
    
    return params

def updateObjectiveFunctionValue(evalMetric):
    """Send Objective Function Value updates to the optimization server"""
    jObj = json.dumps(evalMetric)
    apipath = __SERVER_HOST__  + __SERVER_OBJECTIVE_API__ + "/" + str(__SERVER_SECRET__)
    
    global current_objective
    global pareato_objective
    global rit
    global searchMin

    rit = rit + 1

    current_objective = evalMetric
    if searchMin == True:
        if evalMetric <= pareato_objective: pareato_objective = evalMetric
    elif searchMin == False:
        if evalMetric >= pareato_objective: pareato_objective = evalMetric
    else:
        if evalMetric <= pareato_objective: pareato_objective = evalMetric

    response = requests.post(apipath, json =jObj,verify=False, headers=default_headers )   

    #print(apipath)
    #print(jObj)
    #print(response)

    return response

def getProgress():
    global current_objective
    global pareato_objective
    global rit
    global svr_rit
    return current_objective, pareato_objective, rit, svr_rit 

def getFunctionEvaluations():
    global rit
    global svr_rit
    return rit, svr_rit