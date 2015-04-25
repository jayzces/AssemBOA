# from assemboa import *
from SyntacticAnalyzer import *

# A = Assemboa()
# A.read_and_write('input.in', 'output.out')
S = SyntacticAnalyzer()
S.analyze('input.in')
S.get_token_dictionary('input.in')
print S.token_dictionary