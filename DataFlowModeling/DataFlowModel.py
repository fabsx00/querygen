from collections import defaultdict

class DataFlowModel:
    def __init__(self):
        self.clusterId = -1
        self.members = [] # list of invocation ids of the cluster
        self.sharedSourceClusters = [] # For each arg-group, ids of clusters
        self.numberOfArguments = 0
    
    def setNumberOfArguments(self, n):
        self.numberOfArguments = n
    
    def getNumberOfArguments(self):
        return self.numberOfArguments
    
    def getNumberOfMembers(self):
        return len(self.members) 
    
    def calculateSourcesPerArg(self, invocClusterTool):
        sourceClusters = invocClusterTool.getSourceClusterResult()
        clusterIdToSources = sourceClusters.clusterIdToDatapoint
        
        sourcesPerArg = defaultdict(list)
        
        for x in self.sharedSourceClusters:
            argNum = sourceClusters.clusterIdToArgNum[x]
            sourcesPerArg[argNum].append(clusterIdToSources[x])
        self.sourcesPerArg = sourcesPerArg
        