
import re
from QueryGeneration.RegexGen.TokenAndGapSeq import TokenAndGapSeq

class StringSetToRegex:

    def convert(self, M):
        
        tokenAndGaps = TokenAndGapSeq(M)
        mostVague = tokenAndGaps.mostVagueRegex()
        mostVagueRegex = mostVague.toRegex()
        return mostVagueRegex
                
