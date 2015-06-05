
DEFAULT_MIN_NUM_MEMBERS = 10 # in number of invocations

# This class needs to be replaced by one class
# for data flow model filtering and another
# for data low models decorated with checks.

class ModelSelector:
    
    def __init__(self):
        self.minNumMembers = DEFAULT_MIN_NUM_MEMBERS
        self.callSite = None
        self.topN = None

    def setMinNumMembers(self, val):
        self.minNumMembers = val

    def setCallSite(self, val):
        self.callSite = val

    def setTopN(self, val):
        self.topN = val;

    def setSubChecks(self, val):
        self.subChecks = val

    def select(self, models):

        """
        Select only those models with at least
        self.minNumMembers members that include an
        invocation referring to self.callSite.
        If self.topN is set, select only top N models.
        """

        if self.topN:
            models = models[:self.topN]
        
        retList = []
        for model in models:

            if(model.getNumberOfMembers() <= self.minNumMembers):
                continue

            if(self.callSite and not (self.callSite in model.callSiteIds)):
                continue

            retList.append(model)
        return retList

    def selectForChecks(self, models):
        """
        Select only models referring to one
        of the specified subChecks and the callSite
        of interest.
        """

        retList = []

        for model in models:
            if not model.isRelevant(self.callSite, self.subChecks) :
                continue
            retList.append(model)
        return retList
