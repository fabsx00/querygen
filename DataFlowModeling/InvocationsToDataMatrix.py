
import numpy as np

class InvocationsToDataMatrix:
    
    
    """
    Create a data matrix containing a column
    vector for each invocation.
    """
    
    def convert(self, defStmts, sClusters):

        nClusters = len(sClusters.clusterIdToDatapoint.keys())
        nInvocations = len(defStmts)

        X = np.zeros([nClusters, nInvocations])
        
        for k in range(len(defStmts)):

            stmtsPerArg = defStmts[k]
            
            nGroups = len(stmtsPerArg)
            for i in range(nGroups):
                for dataPoint in stmtsPerArg[i]:
                    coeff = sClusters.dataPointToClusterId[(dataPoint,i)]
                    X[coeff, k] = 1
        
        return X
    