
from scipy.spatial.distance import pdist
from fastcluster import linkage

from ClusterResult import ClusterResult
from scipy.cluster.hierarchy import fcluster
from DataFlowModeling.InvocationsToDataMatrix import InvocationsToDataMatrix


DEFAULT_MAX_DIST_IN_CLUSTER = 2
METRIC = 'cityblock'
LINKAGE_METHOD = 'complete'

class InvocationClusterer:
    
    def __init__(self, contentProvider):
        self.contentProvider = contentProvider
        self.maxDistInCluster = DEFAULT_MAX_DIST_IN_CLUSTER
    
    def setMaxDistInCluster(self, val):
        self.maxDistInCluster = val
    
    def cluster(self, sourceClusters):
        
        self.defStmts = self.contentProvider.getAllDefStmtsPerArg()
        self.sClusters = sourceClusters
        
        converter = InvocationsToDataMatrix()        
        dataMatrix = converter.convert(self.defStmts, self.sClusters)
        
        if dataMatrix.T.shape == (1,1):
            return ClusterResult()
        
        D = pdist(dataMatrix.T, METRIC)
        Z = linkage(D, method= LINKAGE_METHOD)
        
        clustering = fcluster(Z, self.maxDistInCluster, criterion = 'distance')
        result = ClusterResult()

        result.setNumberOfArguments(len(self.defStmts[0]) if len(self.defStmts) > 0 else 0)
        result.registerSet(range(len(self.defStmts)), clustering)
        result.dataMatrix = dataMatrix
        result.callSiteIds = self.contentProvider.getInvocationCallSiteIds()
        
        return result
    
    def getSourceClusterResult(self):
        return self.sClusters
    
