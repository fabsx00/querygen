#!/usr/bin/env python2

import sys, os

cmd = """echo 'getFunctionsByName("%s").functionToAST().match{ it.type == "Condition"}.transform{ "$it.id\t$it.code"}'| joern-lookup -g  """ % (sys.argv[1])

os.system(cmd)
