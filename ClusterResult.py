from collections import defaultdict


class ClusterResult:

    def __init__(self):
        self.dataPointToClusterId = {}
        self.clusterIdToDatapoint = defaultdict(list)
        self.dataMatrix = None
        self.clusterIdToArgNum = {}
        self.numberOfArguments = 0

    def setNumberOfArguments(self, n):
        self.numberOfArguments = n
    
    def getNumberOfArguments(self):
        return self.numberOfArguments

    def registerSet(self, dataPoints, clustering, offset = 0, argNum = 0):
        
        dataPointId = 0
        for x in clustering:
            dataPoint = dataPoints[dataPointId]
            clusterId = x - 1 + offset
            self.register(clusterId, dataPoint, argNum)
            dataPointId += 1
        
    def register(self, clusterId, dataPoint, argNum = 0):
        self.clusterIdToDatapoint[clusterId].append(dataPoint)
        self.dataPointToClusterId[(dataPoint,argNum)] = clusterId
        self.clusterIdToArgNum[clusterId] = argNum