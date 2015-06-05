
from joerntools.mlutils.MLDataDir import MLDataDir
from joerntools.mlutils.pythonEmbedder.PythonEmbedder import Embedder

DIRNAME = "embedding"

class ConditionEmbedder():
    
    def __init__(self, dbContentProvider):
        self.dbContentProvider = dbContentProvider

    
    def embed(self, invocs = [], argNum = None):
        
        # If at this point, we retrieve only vectors for
        # the argument, we can do argument-wise clustering.
        
        X = self.dbContentProvider.getAllCndFeatureVectors(invocs, argNum)
            
        self.dataDir = MLDataDir()
        self.dataDir.create(DIRNAME)
        
        for (cndId, strings) in X:
            self.dataDir.addDataPoint(cndId, strings)
        
        self.dataDir.finalize()
        self.embedder = Embedder()
        self.embedder.embed(DIRNAME, tfidf=True)
        
        return True