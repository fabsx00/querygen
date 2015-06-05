
from ModelSelector import ModelSelector
from CheckModeling.CheckModel import CheckModel
from CheckModeling.ConditionClusterer import ConditionClusterer
from misc import flatten, uniq


DEFAULT_MIN_COND_OBSERVED = 4 # 100
DEFAULT_TOP_N_CHECK_HIST = 10 # 3
DEFAULT_MIN_FRAC_CHECKS = 0.25 # 0.9

class CheckOverlayCreator:
    
    def __init__(self, contentProvider):
        self.contentProvider = contentProvider    
        
        self.minCondObserved = DEFAULT_MIN_COND_OBSERVED
        self.topnCheckHist = DEFAULT_TOP_N_CHECK_HIST
        self.minFracChecks = DEFAULT_MIN_FRAC_CHECKS
    
    def setMinCondObserved(self, val):
        self.minCondObserved = val
    
    def setTopnCheckHist(self, val):
        self.topnCheckHist = val
    
    def setMinFracChecks(self, val):
        self.minFracChecks = val
    
    def createForModels(self, models, onlyForSubChecks = None):

        self.models = [CheckModel(model) for model in models]

        self._generateChecksForAllModels()
        self._retrieveConditions()
        self._distributeChecksPerArg()
                
        self._createConditionClusters()
        
        for model in self.models:
            self.createOverlayForModel(model)
        
        self._filter(onlyForSubChecks)
            
        # self._generateLabels()
        
    
    def _generateLabels(self):
        
        # TODO: Optimization: It's probably possible here to generate node-labels only
        # for those ASTs that are part of one of the models still left.
        
        self.conditionLabels = self.contentProvider.getAllASTNodeLabels()
        for model in self.models:
            model.extractCommonLabels(self.nodeIdToConditionIndex, self.conditionLabels, self.minFracChecks)
        
    
    
    def _createConditionClusters(self):
        
        self.cndClusterTool = ConditionClusterer(self.contentProvider)
        self.conditionClusters = self.cndClusterTool.cluster(self.models)
    
    def createOverlayForModel(self, model):
        
        # Save references to global condition data.
        model.setConditionClusters(self.conditionClusters)
        model.conditionsCode = self.conditionsCode
        model.nodeIdToConditionIndex = self.nodeIdToConditionIndex
        
        model.generateCheckHist()
        model.pruneCheckHist(self.topnCheckHist, self.minCondObserved)
        
    
    def getModels(self):
        return self.models  
    
    def _generateChecksForAllModels(self):
        l = [m.members for m in self.models]
        invocs = uniq(flatten(l))
        
        self.contentProvider.generateChecksForInvocations(invocs)

    def _retrieveConditions(self):

        self.conditions = self.contentProvider.getAllConditions()
        self.nodeIdToConditionIndex = {}
        for i in range(len(self.conditions)):
            self.nodeIdToConditionIndex[self.conditions[i]] = i

        self.conditions = list(set(self.conditions))
        self.conditionsCode = self.contentProvider.getAllConditionsCode()


    def _distributeChecksPerArg(self):
        self.checksPerArg = self.contentProvider.getAllChecksPerArg()
        # list: index is invocation index

        for i in range(len(self.models)):
            for j in range(len(self.models[i].members)):
                self.models[i].checks.append(self.checksPerArg[self.models[i].members[j]])
                # self.models[i].checks.append(self.checksPerArg[j])
    
    def _filter(self, onlyForSubChecks):
        self.modelSelector = ModelSelector()
        self.modelSelector.setSubChecks(onlyForSubChecks)
        self.models = self.modelSelector.selectForChecks(self.models)