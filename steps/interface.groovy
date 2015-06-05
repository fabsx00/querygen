
Object.metaClass.generateTaintLearnStructures = { callSiteIds ->
	generateTaintGraphs(callSiteIds);
}

/**
 * Generates global list 'taintGraphs' that contains one taint-graph
 * for each call-site.
 * */


Object.metaClass.generateTaintGraphs = { callSiteIds ->
	
	resetTaintGraphs()
	createTaintGraphs(callSiteIds)
	println taintGraphs
}

Object.metaClass.resetTaintGraphs = {
	
	// Note: Trying to set taintGraphs to [] fails.
	// Clearing it works.
	
	if(!Object.metaClass.hasProperty('taintGraphs')){
		Object.metaClass.taintGraphs = []
	}
	
	Object.metaClass.taintGraphs.clear()
}

Object.metaClass.createTaintGraphs = { callSiteIds ->
	
	def allTaintGraphs = callSiteIds.collect{
		tGraph = createInitGraph(it);
		tGraph.invocations = decompressInitGraph(tGraph)
		tGraph
	}
	
	taintGraphs.addAll(allTaintGraphs)
}


/**
 * Get a flat ist of all API symbols used in def-statements
 * */

Object.metaClass.getSourceAPISymbols = {
		
	println 'getSourceAPISymbols'
	
	def acc = []
	def s = taintGraphs[0].invocations[0].defStmtsPerArg.size()
		
	taintGraphs.each{ tGraph ->
		tGraph.invocations.each{
			it.defStmtsPerArg.eachWithIndex{ x, i ->
				
				if(acc.size() <= i){ acc << []}
				 
				acc[i].addAll(x)
				acc[i].sort()
			}
		}
	}

	acc.eachWithIndex{ a, i -> acc[i].unique() }

	acc._().transform{
		idListToNodes(it).apiSyms().dedup().toList()
	}.toList()
	
}

Object.metaClass.getAllDefStmtsPerArg = {

	println 'getAllDefStmtsPerArg'
	
	def acc = []
	
	taintGraphs.each{ tGraph ->
		tGraph.invocations.each{
			acc << it.defStmtsPerArg.collect{ idListToNodes(it).apiSyms().dedup().toList()}
		}
	}
	acc
	// acc.unique()
}

Object.metaClass.getAllChecksPerArg = {
	println 'getAllChecksPerArg'
	
	c = { it.checksPerArg.id }
	collectForInvocations(c)
}


Object.metaClass.getAllCndFeatureVectors = { argNum = null ->
	
	println 'getAllCndFeatureVectors'
	
	def asts = 	collectForInvocations{
		if(argNum != null)
			it.checksPerArg[argNum]
		else
			it.checksPerArg
	}.flatten().unique{ a, b -> a.id <=> b.id }

	.collect{ [it.id, it.normalizedAST] }	
	
	 mapToVectors(asts)
}

Object.metaClass.getCndFeatureVectorsForInvocs = { invocIds, argNum = null ->
	
	println 'getCndFeatureVectorsForInvocs'
	
	// this can be done more efficiently

	def i = 0;
	def invocs = taintGraphs.collect{ tGraph ->
		tGraph.invocations.collect{
			i ++;
			if(i -1 in invocIds)
				[it]
			else
				[]
		}
	}.flatten()

	def asts = 	invocs.collect{
		if(argNum != null)
			if(it.checksPerArg[argNum])
				it.checksPerArg[argNum]
			else
				[]
		else
			it.checksPerArg
	}.flatten().unique{ a, b -> a.id <=> b.id }

	.collect{ [it.id, it.normalizedAST] }
	
	 mapToVectors(asts)
}


Object.metaClass.getAllConditions = {
	
	println 'getAllConditions'
	
	// this seems to be the same as get getAllChecksPerArg
	// except for the 'flatten' and 'unique' part.
	
	collectForInvocations{
		it.checksPerArg
	}.flatten().unique{ a, b -> a.id <=> b.id }
	.id
}

Object.metaClass.getAllConditionsCode = {

	println 'getAllConditionsCode'
	
	collectForInvocations{
		it.checksPerArg
	}.flatten().unique{ a, b -> a.id <=> b.id }
	.collect{ it.getCode() }
	.toList();
}

Object.metaClass.getAllASTNodeLabels = {

	println 'getAllASTNodeLabels'
	
	def x = collectForInvocations{
		it.checksPerArg
	}.flatten().unique{ a, b -> a.id <=> b.id }
	.normalizedAST.collect(){ labelsFromAST(it) };
	x
}

Object.metaClass.getControlledSinks = { nodeId ->

    def nodeSet = []
    def nodesToExpand = [g.v(nodeId)]
	
    for(i in 0 .. 2){
		def newNodes = nodesToExpand._().out("CONTROLS").toList();
		newNodes.addAll(newNodes._().expandArguments().out("REACHES").filter{it.type == 'Condition'}.toList())
		nodeSet.addAll(newNodes)
		nodesToExpand = newNodes.collect()
	}
		
    nodeSet._().match{it.type == 'Callee'}
    .transform{ [it.code, it.calleeToCall().id.toList()[0] ] }
     .toList()
}


Object.metaClass.getInvocationCallSites = {
	def acc = []
	
	taintGraphs.collect{ tGraph ->
		def callSiteId = tGraph.callSiteId
		tGraph.invocations.each{
			acc << callSiteId;
		}
	}
	acc
}

Object.metaClass.generateChecksForInvocations = { invocs ->
	
	def allInvocs = collectForInvocations{ it };
	
	allInvocs[invocs].each{
		it.checksPerArg = genConditionsPerArg(it.allGraphlets, it.graphletIds)
	}
}
