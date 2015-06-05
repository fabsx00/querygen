
/**
   For a given parameter (String), determine all
   parameter to sink systems (only intraprocedural).
*/

Object.metaClass.paramSinkSystems = { paramCode, order = 1 ->
	
	luceneQuery = String.format("type:Parameter AND code:\"%s\"", paramCode)
	
	queryNodeIndex(luceneQuery)
	.sideEffect{ srcId = it.id; }
	.argSinks(order)
	.sideEffect{argNum = it.childNum; }	
	.sideEffect{ snkId = it.id }
	.argToCall().callToCallee()
	.transform{ String.format("%s\t%s\t%s\t%s",it.code, argNum, srcId, snkId) }
}

/**
 From a statement node, determine tainted arguments of calls.
*/

Gremlin.defineStep('argSinks', [Vertex,Pipe], { order = 1 ->
	_()
	.as('x')
	.statements()
	.outE('REACHES').sideEffect{ symbol = it.var; }
	.inV().match{ it.type == 'Argument'}
	.loop('x'){ it.loops <= order}{
		// keep node, if ...
		it.object.filter{ symbol in it.uses().code.toList() }
		.toList() != []
	}
	.dedup()
})

Gremlin.defineStep('functionToCallers', [Vertex,Pipe], {
	_().transform{
		getCallsTo(it.name)
	}.scatter()
})
