
from joerntools.misc.launch import launch
from ClusterResult import ClusterResult
from CheckModeling.ConditionEmbedder import ConditionEmbedder
import os

class ConditionClusterer:
    
    def __init__(self, contentProvider):
        self.contentProvider = contentProvider
    
    def cluster(self, models):

        retval = ClusterResult()
        
        for model in models:
            for argNum in range(model.getNumberOfArguments()):
                
                invocs = model.members
                curOffset = len(retval.clusterIdToDatapoint.keys())
                
                embedder = ConditionEmbedder(self.contentProvider)
                embedder.embed(invocs, argNum)
                
                # TODO: we need to be able to pass a distance parameter to joern-cluster
                clusterLines = [x.rstrip() for x in launch('joern-cluster')]
                clustering = []
                datapoints = []
                
                for line in clusterLines:
                    (nodeId, clusterId) = line.split('\t')
                    clustering.append(int(clusterId))
                    datapoints.append(nodeId)
        
                retval.registerSet(datapoints, clustering, curOffset, argNum)
                
                os.system('rm -rf embedding')
        
        return retval
