from DBContentsProvider import DBContentsProvider

from PatchAnalysis.CheckToSinks import CheckToSinks
from PatchAnalysis.CheckToSubChecks import CheckToSubChecks
from DataFlowModeling.DataFlowModelCreator import DataFlowModelCreator
from CheckModeling.CheckOverlayCreator import CheckOverlayCreator
from QueryGeneration.ModelToQuery import ModelToQuery
from Debug.ModelPrinter import ModelPrinter

class APIFuncToQueries:
    
    def run(self, checkId):

        contentProvider = DBContentsProvider()    
        check2SubChecks = CheckToSubChecks(contentProvider) 
        subChecks = check2SubChecks.checkToSubChecks(checkId)
        
        check2Sinks = CheckToSinks(contentProvider)
        sinks = check2Sinks.checkToSink(checkId)
        
        print sinks
        if not sinks:
            print 'No sinks.'
            sys.exit()
            
        modelCreator = DataFlowModelCreator(contentProvider)
        overlayCreator = CheckOverlayCreator(contentProvider)
        
        for sink in sinks:
            sinkSymbol, callSiteId = sink
            
            if 'log' in sinkSymbol: continue
            print sinkSymbol
            
            modelCreator.createDataFlowModels(sinkSymbol, callSiteId)
            models = modelCreator.getModels()
            
            overlayCreator.createForModels(models, subChecks)
            models = overlayCreator.getModels()
            
            converter = ModelToQuery()
            for query in [converter.convert(model) for model in models]:
                print query
            
            # modelPrinter = ModelPrinter()
            # modelPrinter.printSummary(models)    
            # modelPrinter.printAll(models)


if __name__ == '__main__':

    import sys
    checkId = sys.argv[1]
    
    tool = APIFuncToQueries()
    tool.run(checkId)
    
    