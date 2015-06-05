from joern.all import JoernSteps


class DBContentsProvider:

    def __init__(self):
        self._initDatabaseConnection()

    def _initDatabaseConnection(self):
        
        self.j = JoernSteps()
        self.j.connectToDatabase()
        self.j.addStepsDir('steps/')
    
    """
    Generate contents for a given selector, overwriting
    the contents currently held in cndToQueries memory by the server.
    """
    def generate(self, selector):
        query = """generateTaintLearnStructures(%s.id.toList())
        _()""" % (selector)
        for unused in self.j.runGremlinQuery(query): pass
    
    def generateChecksForInvocations(self, invocs):
        query = """generateChecksForInvocations(%s.toList())
        _()""" % (invocs)
        
        for unused in self.j.runGremlinQuery(query): pass
    
    # Source Analysis
    
    def getSourceAPISymbols(self):
        query = """_().transform{ getSourceAPISymbols() }.scatter() """
        return [x for x in self.j.runGremlinQuery(query)]
    
    def getAllDefStmtsPerArg(self):
        query = """_().transform{ getAllDefStmtsPerArg() }.scatter() """
        return [x for x in self.j.runGremlinQuery(query)]
    
    # Condition Analysis
    
    def getAllChecksPerArg(self):
        query = """_().transform{ getAllChecksPerArg() }.scatter() """
        return [x for x in self.j.runGremlinQuery(query)]
    
    def getAllConditions(self):
        query = """_().transform{ getAllConditions() }.scatter() """
        return [x for x in self.j.runGremlinQuery(query)]
    
    def getAllConditionsCode(self):
        query = """_().transform{ getAllConditionsCode() }.scatter() """
        return [x for x in self.j.runGremlinQuery(query)]
    
    def getInvocationCallSiteIds(self):
        query = """_().transform{ getInvocationCallSites() }.scatter() """
        return [x for x in self.j.runGremlinQuery(query)]
      
    def getSubConditions(self, nodeId):
        query = """_().transform{ subConditions(%s) }.scatter() """ % (nodeId)
        return [x for x in self.j.runGremlinQuery(query)]
    
    def getAllCndFeatureVectors(self, invocs = [], argNum = None):
        
        if not invocs:
            if argNum != None:
                query = """_().transform{ getAllCndFeatureVectors(%d) }.scatter() """ % (argNum)
            else:
                query = """_().transform{ getAllCndFeatureVectors() }.scatter() """
        
        else:
            if argNum != None:
                query = """_().transform{ getCndFeatureVectorsForInvocs(%s, %d) }.scatter() """ % (invocs, argNum)
            else:
                query = """_().transform{ getCndFeatureVectorsForInvocs(%s) }.scatter() """ % (invocs)
        
        return [x for x in self.j.runGremlinQuery(query)]

    def getAllASTNodeLabels(self):
        query = """_().transform{ getAllASTNodeLabels() }.scatter() """
        return [x for x in self.j.runGremlinQuery(query)]
    
    # Choosing sinks
    
    def getControlledSinks(self, nodeId):
        query = """_().transform{ getControlledSinks(%s) }.scatter() """ % (nodeId)
        return [x for x in self.j.runGremlinQuery(query)]
  
    
    
if __name__ == '__main__':
    gen = DBContentsProvider()
    # gen.generate('g.v(12798)._()')
    gen.generate('getCallsTo("TIFFFetchData")._()')
    for x in gen.getSourceAPISymbols():
        print x