
class CheckToSubChecks:
    
    def __init__(self, contentProvider):
        self.contentProvider = contentProvider
    
    def checkToSubChecks(self, checkId):
        return self.contentProvider.getSubConditions(checkId)
    
    

