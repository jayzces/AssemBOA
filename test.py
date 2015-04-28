# from assemboa import *
from syntactic_analyzer import *
from semantic_analyzer import *

# A = Assemboa()
# A.read_and_write('input.in', 'output.out')
syntactic = SyntacticAnalyzer()
syntactic.analyze('input.in')
syntactic.get_token_dictionary('input.in')
semantic = SemanticAnalyzer(syntactic.token_dictionary)
semantic.generate_symbol_table()
semantic.analyze('input.in')