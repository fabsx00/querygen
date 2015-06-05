from misc import uniqListOfLists

class CheckToSinks:    
    
    def __init__(self, dbContentProvider):
        self.contentProvider = dbContentProvider
    
    def checkToSink(self, checkId):
        retval = self.contentProvider.getControlledSinks(checkId)
        return uniqListOfLists(retval)