
from Levenshtein import jaro as jd  # @UnresolvedImport
from fastcluster import linkage
from scipy.cluster.hierarchy import fcluster
from ClusterResult import ClusterResult

DEFAULT_MAX_DIST_IN_CLUSTER = 0.2
DEFAULT_LINKAGE_METHOD = 'average'

class SourceClusterer:
    
    def __init__(self, contentProvider):
        self.contentProvider = contentProvider
        self.maxDistInCluster = DEFAULT_MAX_DIST_IN_CLUSTER
        self.linkageMethod = DEFAULT_LINKAGE_METHOD
    
    def setMaxDistInCluster(self, val):
        self.maxDistInCluster = val
    
    def setLinkageMethod(self, val):
        self.linkageMethod = val
    
    def cluster(self):
        
        # We cluster for each argument independently!        
        retval = ClusterResult()
        
        curOffset = 0
        argNum = 0
        for symbolsForArg in self.contentProvider.getSourceAPISymbols():
            D = self._calculateDistanceMatrix(symbolsForArg)

            curOffset = len(retval.clusterIdToDatapoint.keys())

            if len(symbolsForArg) == 0:
                argNum += 1
                continue
            
            if len(symbolsForArg) == 1:
                retval.register(curOffset, symbolsForArg[0], argNum)
                argNum += 1
                continue
            
            Z = linkage(D, method=self.linkageMethod)
            clustering = fcluster(Z, self.maxDistInCluster, criterion = 'distance')
            
            retval.registerSet(symbolsForArg, clustering, curOffset, argNum)
            argNum += 1
        
        return retval
     
    def _calculateDistanceMatrix(self, symbolsForArg):
        
        nSymbols = len(symbolsForArg)
        
        D = [1 - jd(symbolsForArg[x], symbolsForArg[y])
                for x in xrange(nSymbols) for y in xrange(x+1,nSymbols)]
        return D
        
if __name__ == '__main__':
    from DBContentsProvider import DBContentsProvider
    
    selector = 'getCallsTo("TIFFFetchData")._()'
    contentProvider = DBContentsProvider()
    contentProvider.generate(selector)
    tool = SourceClusterer(contentProvider)
    print tool.cluster()
    