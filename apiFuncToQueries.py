from DBContentsProvider import DBContentsProvider

from DataFlowModeling.DataFlowModelCreator import DataFlowModelCreator
from CheckModeling.CheckOverlayCreator import CheckOverlayCreator
from QueryGeneration.ModelToQuery import ModelToQuery
from Debug.ModelPrinter import ModelPrinter

class APIFuncToQueries:
    
    def run(self, sinkSymbol):

        contentProvider = DBContentsProvider()    
            
        modelCreator = DataFlowModelCreator(contentProvider)

        modelCreator.setSourceDistInCluster(0.2)
        modelCreator.setInvocDistInCluster(3)
        modelCreator.setMinNumMemersInInvocCluster(4)

        modelCreator.setTopnInvocClusters(10000)
        
        modelCreator.createDataFlowModels(sinkSymbol)
        models = modelCreator.getModels()
 
        overlayCreator = CheckOverlayCreator(contentProvider)
        overlayCreator.setMinCondObserved(3) # <- changed from 4 
        overlayCreator.setMinFracChecks(10) # <- changed from 10 # NOT USED!
        overlayCreator.setTopnCheckHist(10) # <- changed from 10
        overlayCreator.createForModels(models)
        models = overlayCreator.getModels()
        
        modelPrinter = ModelPrinter()
        # modelPrinter.printSummary(models)    
        # modelPrinter.printAll(models)

        converter = ModelToQuery()
        
        for model in models:
            query = converter.convert(model)
            # print 'ClusterId: ' + str(model.clusterId)
            print query

if __name__ == '__main__':

    import sys
    apiFunc = sys.argv[1]
    
    tool = APIFuncToQueries()
    tool.run(apiFunc)
    
    
