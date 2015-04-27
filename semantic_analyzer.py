import string

class SemanticAnalyzer(object):
    def __init__(self, token_dictionary):
        super(SemanticAnalyzer, self).__init__()
        self.token_dictionary = token_dictionary
        self.symbol_table = []
        self.symbol_table.append([])
        self.current_row_index = 0


    def generate_symbol_table(self, token_dictionary):
    	# for row in self.token_dictionary:
    		