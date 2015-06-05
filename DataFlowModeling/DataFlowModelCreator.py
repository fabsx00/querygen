
from SourceClusterer import SourceClusterer
from DataFlowModeling.DataFlowModel import DataFlowModel
from ModelSelector import ModelSelector
import numpy as np
from DataFlowModeling.InvocationClusterer import InvocationClusterer

DEFAULT_SOURCE_DIST_IN_CLUSTER = 0.2    # jaro distance
DEFAULT_INVOC_DIST_IN_CLUSTER = 4       # cityblock
DEFAULT_MIN_NUM_MEMBERS_IN_INVOC_CLUSTER = 100
DEFAULT_TOPN_INVOC_CLUSTERS = 20 # 3


class DataFlowModelCreator:
    
    def __init__(self, contentProvider):
        self.contentProvider = contentProvider
        
        self.sourceDistInCluster = DEFAULT_SOURCE_DIST_IN_CLUSTER
        self.invocDistInCluster = DEFAULT_INVOC_DIST_IN_CLUSTER
        self.minNumMembersInInvocCluster = DEFAULT_MIN_NUM_MEMBERS_IN_INVOC_CLUSTER
        self.topnInvocClusters = DEFAULT_TOPN_INVOC_CLUSTERS
    
    def setSourceDistInCluster(self, val):
        self.sourceDistInCluster = val
    
    def setInvocDistInCluster(self, val):
        self.invocDistInCluster = val
    
    def setMinNumMemersInInvocCluster(self, val):
        self.minNumMembersInInvocCluster = val
    
    def setTopnInvocClusters(self, val):
        self.topnInvocClusters = val
    
    def createDataFlowModels(self, sinkSymbol, onlyForCallSite = None):
           
        self.selector = self._sinkSymbolToSelector(sinkSymbol)
        
        self._createForSelector()
        self._filter(onlyForCallSite)
        
        for model in self.models:
            model.calculateSourcesPerArg(self.invocClusterTool)
    
    def getModels(self):
        return self.models  



    def _sinkSymbolToSelector(self, sinkSymbol):
        return 'getCallsTo("%s")' % (sinkSymbol)
    
    def _createForSelector(self):
        
        self.contentProvider.generate(self.selector)
        
        # Cluster source API symbols using jaro distance.
        
        self.sourceClusterer = SourceClusterer(self.contentProvider)
        self.sourceClusterer.setMaxDistInCluster(self.sourceDistInCluster)
        sourceClusters = self.sourceClusterer.cluster()
        
        # Cluster invocations based on source-argument mappings.
        
        self.invocClusterTool = InvocationClusterer(self.contentProvider)
        self.invocClusterTool.setMaxDistInCluster(self.invocDistInCluster)
        self.invocClusters = self.invocClusterTool.cluster(sourceClusters)
        
        self._createModelsFromInvocClusters(self.invocClusters)
    
    def _createModelsFromInvocClusters(self, invocClusters):

        X = invocClusters.dataMatrix

        self.models = []
        for (clusterId, invocIds) in invocClusters.clusterIdToDatapoint.iteritems():
            newModel = DataFlowModel()
            newModel.clusterId = clusterId
            newModel.members = invocIds
            # We need to add 1 here for the 'other' group
            newModel.setNumberOfArguments(invocClusters.getNumberOfArguments() + 1)
            newModel.callSiteIds = [invocClusters.callSiteIds[x] for x in invocIds]
            newModel.sharedSourceClusters = np.nonzero(np.sum(X[:, tuple(newModel.members)], axis=1) > 0.5* len(invocIds))[0]
            newModel.selector = self.selector
            self.models.append(newModel)

        # Sort models by number of members
        self.models.sort(key=lambda x: len(x.members), reverse=True)
    
    def _filter(self, onlyForCallSite):
        
        self.modelSelector = ModelSelector()
        
        self.modelSelector.setCallSite(onlyForCallSite)
        self.modelSelector.setMinNumMembers(self.minNumMembersInInvocCluster)
        self.modelSelector.setTopN(self.topnInvocClusters)
        
        self.models = self.modelSelector.select(self.models)
        
    