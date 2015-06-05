
LABEL_MASK = 0xffff
LABEL_WIDTH = 16 // TODO: calculate this from mask


Object.metaClass.mapToVectors = { asts ->
	
	asts.collect{
		def labels = NH(NH(CndNHGraph(it[1])))[1]
		[it[0], labels.values() ]
	}
}

Object.metaClass.CndNHGraph = { astNode ->
	
	def children = [:]
	def labels = [:]
	
	def nodes = allASTNodes(astNode)
	
	def X = nodes.collect{ [it.id, hashVal(it.label), it.children.id] }
	
	for (x in X){
		nodeId = x[0]
		label = x[1]
		childIds = x[2]
		
		children[nodeId] = childIds
		labels[nodeId] = label
	}

	[children, labels]
}
