
Object.metaClass.labelsFromAST = { it ->
	def stack = []
	_labelsFromAST(it, stack)
}

Object.metaClass._labelsFromAST = { thisNode, stack ->
	
	if(thisNode.children.size() == 0){
		if(stack.contains('EqualityExpression') ||
		   stack.contains('RelationalExpression') ||
           stack.contains('UnaryOp')
        ){
			
		   if(thisNode.label != '_ARG_')
				return [String.format('check\t"%s"', thisNode.label)]
			else
				return ["check\ts"]
		}
		return []
	}else{
		thisNode.children.collect{ _labelsFromAST(it, stack.plus(thisNode.label) )}.flatten()	
	}
	
}