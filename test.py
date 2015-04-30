# from assemboa import *
from syntactic_analyzer import *
from semantic_analyzer import *
from code_translator import *
from computer import *

# A = Assemboa()
# A.read_and_write('input.in', 'output.out')
file_to_read = 'input.in'
file_to_write = 'output.out'

syntactic = SyntacticAnalyzer()
syntactic.analyze(file_to_read)
semantic = SemanticAnalyzer(syntactic.token_dictionary)
semantic.analyze(file_to_read)
code_translator = CodeTranslator(syntactic.token_dictionary, semantic.symbol_table)
code_translator.translate(file_to_write)
computer = Computer()
computer.execute(file_to_write, True)
for item in computer.exec_log:
    print item
