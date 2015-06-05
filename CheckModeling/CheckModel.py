

from collections import defaultdict, Counter
from DataFlowModeling.DataFlowModel import DataFlowModel


class CheckModel(DataFlowModel):
    
    def __init__(self, dataFlowModel):
        self._setDataFlowModelAttributes(dataFlowModel)
        
        self.conditionClusters =  None
        self.checks = []
 
    def _setDataFlowModelAttributes(self, dataFlowModel):
        for k, value in dataFlowModel.__dict__.iteritems():
            setattr(self, k, value )

    def setConditionClusters(self, conditionClusters):
        self.conditionClusters = conditionClusters
        
    def generateCheckHist(self):
        """
        count how often each check-cluster occurs
        and save checkClusterIds
        """
        
        self.checkHist = defaultdict(lambda: defaultdict(int))
        self.topCheckHists = []
        
        # checkvec contains a list of node ids for
        # each argument.
        
        # uniqDatapoints = defaultdict(set)
        uniqDatapoints = defaultdict(list)
        
        for checkVec in self.checks:
            nArgs = len(checkVec)
            for i in range(nArgs):
                for datapoint in checkVec[i]:
                    uniqDatapoints[i].append(datapoint)
                    # uniqDatapoints[i].add(datapoint)
        
        for i in range(nArgs):
            for datapoint in uniqDatapoints[i]:
                clusterId = self.conditionClusters.dataPointToClusterId[(datapoint,i)]
                self.checkHist[i][clusterId] += 1

        
#         for checkVec in self.checks:
#             nArgs = len(checkVec)
#             for i in range(nArgs):
#                 for datapoint in checkVec[i]:
#                     
#                     clusterId = self.conditionClusters.dataPointToClusterId[datapoint]
#                     self.checkHist[i][clusterId] += 1
      
        # checkHist[i][clusterId] is then the number
        # of occurrences of clusterId for argument i.

    def pruneCheckHist(self, topN, minCondObserved):

        for i in range(len(self.checkHist.keys())):
            checkHistForArg = self.checkHist[i]
            
            sortedCheckHist = sorted(checkHistForArg.iteritems(), key = lambda x: x[1], reverse=True)[:topN]
            sortedCheckHist = [x for x in sortedCheckHist if x[1] >= minCondObserved]
            
            # sortedCheckHist = [x for x in sortedCheckHist]
            
            self.topCheckHists.append(sortedCheckHist)
    
              
    def extractCommonLabels(self, nodeIdToConditionIndex, conditionLabels, minFracChecks):
        
        # topHistogram is a list containing one entry for each argument.
        # Each entry is a sorted list of (clusterId, occ) pairs
        
        self.nodeIdToConditionIndex = nodeIdToConditionIndex
        self.conditionLabels = conditionLabels
        
        commonLabels = []
        
        # For each argument
        
        for i in range(len(self.topCheckHists)):
            topCheckHistForArg = self.topCheckHists[i]
            commonLabels.append({})
            
            for (clusterId,nOcc) in topCheckHistForArg:
                
                
                # Add labels of all conditions in each of the clusters.
                # This may be problematic as it includes labels from
                # conditions, which were never even used in this context.
                
                labels = [self.conditionLabels[self.nodeIdToConditionIndex[y]] for y in self.conditionClusters.clusterIdToDatapoint[clusterId]]
                labels = labels * nOcc
                labels = [x for sublist in labels for x in sublist]
                c = Counter(labels)
                
                nConditionNodes = len(self.conditionClusters.clusterIdToDatapoint[clusterId]) 
                total = nOcc * nConditionNodes
                
                for key in c:
                    c[key] = float(c[key]) / float(total)
                
                commonLabels[i][clusterId] = [(x,y) for (x,y) in c.most_common() if y > minFracChecks]
                
        
        self.commonLabels = commonLabels
    
    # This should be moved into selector.
    
    def isRelevant(self, onlyForCallSite = None, onlyForSubChecks = None):
        
        if onlyForCallSite:
            if not onlyForCallSite in self.callSiteIds:
                return False
        
        if onlyForSubChecks:
            if not self._refersToChecks(onlyForSubChecks):
                return False
        
        return True
    
    def _refersToChecks(self, onlyForSubChecks):

        for topCheckHist in self.topCheckHists:
            for (clusterId, nOcc) in topCheckHist:
                
                checksInCluster = set(self.conditionClusters.clusterIdToDatapoint[clusterId])
                checksInCluster = [long(x.split('[')[0]) for x in checksInCluster]                
                if(set(checksInCluster).intersection(set(onlyForSubChecks)) != set([])):
                    return True
            
        return False
    