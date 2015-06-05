
from collections import defaultdict
from misc import uniqListOfLists

OUTPUT_TRANSFORMATION = """
.transform{ sink = g.v(it.allGraphlets[it.graphletIds[0]].args[0]).statements().id.toList()[0];it.defStmtsPerArg}
.transform{ sink }
"""

class ModelToQuery:

    def convert(self, model):

        nArgs = model.getNumberOfArguments()

        argSources = self._createArgSourceDescriptions(model)
        
        if hasattr(model, "topCheckHists"):
            argChecks = self._createArgCheckDescriptions(model)

        query = '/* =============== */\n'
        query += self._addSourceVariables(argSources)
        if hasattr(model, "topCheckHists"):
            query += self._addSanitizerVariables(argChecks)
        query += self._addTaintedArgSteps(argSources, model)
        if hasattr(model, "topCheckHists"):
            query += self._addUnsanitizedSteps(argChecks, argSources, nArgs)

        query = query + OUTPUT_TRANSFORMATION
        # query = query.replace('\n', ' ')
        return query
        # return self._escape(query)


    def _addSourceVariables(self, argSources):

        query = ''

        for i in argSources.keys():
            if argSources[i] == []: continue

            for j in range(len(argSources[i])):
                query += "arg%d%dSource = sourceMatches('%s');\n" % (i, j, self.escapeIt(argSources[i][j]))

        return query

    def _addSanitizerVariables(self, argChecks):

        query = ''
        for check in argChecks:
            if check == '': continue
            query += check
        return query

    def _addTaintedArgSteps(self, argSources, model):

        query = "\n" + model.selector + "\n"

        nargs = model.getNumberOfArguments() - 1
                
        argSourceDescrs = []
        for i in xrange(nargs):
            if(not argSources.has_key(i)):
                argSourceDescrs.append('ANY_SOURCE')
            else:
                x = '{' + ('&&\n'.join(['arg%d%dSource(it)' % (i,j) for j in range(len(argSources[i]))]) ) + '}'
                argSourceDescrs.append(x)
             
        
        query += '.taintedArgs([' + (','.join(argSourceDescrs)) + '])'
        return query

    def escapeIt(self,x ):
        x = x.replace(' . ', ' \\\. ')
        x = x.replace(' * ', ' \\\* ')
        x = x.replace(' ( ', ' \\\( ')
        x = x.replace(' )', ' \\\)')
        x = x.replace(' [ ', ' \\\[ ')
        x = x.replace(' ]', ' \\\]')
        x = x.replace('\d+', '\\\\d+')
        return x
        

    def _addUnsanitizedSteps(self, argChecks, argSources, nArgs):

        sanitizers = []

        if len(argChecks) == 0:
            return ''


        reached = False
        for i in range(nArgs - 1):
            if argChecks[i] == '':
                sanitizers.append('null')
            else:
                reached = True
                s = argChecks[i]
                s = s[:s.find('=')]
                sanitizers.append(s)
        
        if not reached:
            return ''
        
        s = (','.join(sanitizers))
        # if s == 'null': s = ''
        s = '\n.unchecked([' + s + '])'
        return s
    
    def _createArgSourceDescriptions(self, model):
        
        
        argSources = defaultdict(list)
            
        for argNum in model.sourcesPerArg.keys():
            
            clusters = model.sourcesPerArg[argNum]
            for cluster in clusters:
                srcRegex = self._clusterToRegex(cluster) 
                argSources[argNum].append(srcRegex)
        
        return argSources        
        
    
    def _createArgCheckDescriptions(self, model):
        
        argChecks = [] # one element per argument
        retval = []
        
        # Note: we subtract 1 here so that we don't output
        # the cluster that is unbound to any of the args.
        nArgs = model.getNumberOfArguments() -1

        
        if(model.topCheckHists == [[]]):
            l = []
            for i in range(nArgs):
                l.append('')
            return l
        
        for i in range(nArgs):
        
        # for i in range(len(model.topCheckHists) - 1):    
        # for i in range(len(model.topCheckHists)):
            
            try:
                topCheckHist = model.topCheckHists[i]
            except IndexError:
                return []

            argChecks.append([])
            
            for (clusterId,nOcc) in topCheckHist:
                
                condCode = [model.conditionsCode[model.nodeIdToConditionIndex[y]]
                            for y in model.conditionClusters.clusterIdToDatapoint[clusterId]]
                                
                argChecks[-1].append(condCode)


            checksForArg = uniqListOfLists(argChecks[-1])
            
            if checksForArg == []:
                retval.append('')
                continue
            
            conditionStrs = []
            for conditionCluster in checksForArg:
                cndRegex = self._conditionsToRegex(conditionCluster)

                cndRegex = '"%s"' % (cndRegex)
                conditionStrs.append(self.escapeIt('\n it.code.matches(String.format(%s, Pattern.quote(s)))' % cndRegex))
                
            retval.append('arg%dSanitizer = { it, s -> ' % (i) +   "||".join(conditionStrs) + '\n};\n')
        
        return retval
    
    def _clusterToRegex(self, cluster):
        if len(cluster) == 1:
            srcRegex = '.*' + cluster[0] + '.*'
        else:
            from QueryGeneration.RegexGen.StringSetToRegex import StringSetToRegex
            converter = StringSetToRegex()
            srcRegex = converter.convert(cluster)
        return srcRegex
    

    def _convertSpecialSyms(self, c):
        c = c.replace('QUERYGEN_ARG', '%s')
        c = c.replace('QUERYGEN_REL', '[<>]=?')
        c = c.replace('QUERYGEN_EQ', '(==|!=)')          
        return c
        
    def _conditionsToRegex(self, conditionCluster):
        cluster = [self._convertSpecialSyms(c) for c in conditionCluster]
        return self._clusterToRegex(cluster)
        