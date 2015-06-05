

class ModelPrinter:
    
    def printSummary(self, models):
        self.models = models

        nModels = len(self.models)

        print "-- Model Summary --"
        print "===================="
        print 'Number of models: %d' % (nModels)
        print ''

        nInvocations = sum([model.getNumberOfMembers() for model in self.models])

        print 'Number of invocations: %d' % (nInvocations)
        print "--------------------------"

        for model in self.models:
            print 'In cluster %d: %d ' % (model.clusterId , model.getNumberOfMembers())

        print "--------------------------"

    
    def printAll(self, models):

        self.printSummary(models)
        
        print 'Model contents'

        for model in self.models:
            self.printModel(model)
        
    
    def printModel(self, model):
             
                    
        print '====================='
        print 'Cluster Id: %d' % (model.clusterId)
        print 'Number of unique Callsites: %d' % (len(list(set(model.callSiteIds))))
        print 'CallSiteIds: %s' % (str(list(set(model.callSiteIds))))
        print '====================='
          
        for argNum in sorted(model.sourcesPerArg):
            print 'Shared sources for argument %d: %s'  % (argNum, model.sourcesPerArg[argNum])
        
        if hasattr(model,'topCheckHists') and model.topCheckHists:
            self.printChecksForModel(model)
        
        print '====================='
    
    
    def printChecksForModel(self, model):
        
        self.conditionClusters = model.conditionClusters
        self.conditionsCode = model.conditionsCode
        self.nodeIdToConditionIndex = model.nodeIdToConditionIndex
        
        for i in range(len(model.topCheckHists)):
            print 'Top Checks for Argument %d:' % (i)
            topCheckHistForArg = model.topCheckHists[i]
            
            for (clusterId,nOcc) in topCheckHistForArg:
                
                nConditionNodes = len(self.conditionClusters.clusterIdToDatapoint[clusterId])                
                # print '----- %d ----' % (nOcc * nConditionNodes)
                print '----- %d ----' % (nOcc)

                print 'Condition node IDs: %s' % (str(self.conditionClusters.clusterIdToDatapoint[clusterId]))
                
                # labels = model.commonLabels[i][clusterId]
                # self._printLabels(labels)
                
                condCode = [self.conditionsCode[self.nodeIdToConditionIndex[y]] for y in self.conditionClusters.clusterIdToDatapoint[clusterId]]
                condCode = set(condCode)
                for c in condCode:
                    print c
                
                print '-----'
    
    
    def _printLabels(self, labels):
        print 'Labels'
        print '======='
        for label in labels:
            print label
        
        print '=============='
    
