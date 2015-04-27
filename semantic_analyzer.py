import string

class SemanticAnalyzer(object):
    def __init__(self, token_dictionary):
        super(SemanticAnalyzer, self).__init__()
        self.token_dictionary = token_dictionary
        self.symbol_table = [[]]
        self.current_row_index = 0
        self.current_mem_space = 0

    def generate_symbol_table(self):
        self.get_labels()
        for token, token_type in self.token_dictionary.iteritems():
            if token_type == 'identifier':
                if self.current_row_index != 0:
                    if not token in (li[0] for li in self.symbol_table):
                        if self.current_mem_space < 10:
                            row = []
                            row.append(token)
                            row.append(token_type)
                            row.append('0' + str(self.current_mem_space))
                            self.symbol_table.append(row)
                            self.current_row_index += 1
                            self.current_mem_space += 1
                        else:
                            return 'Fatal Error: Out of Memory.'
                else:
                    if self.current_mem_space < 10:
                            self.symbol_table[0].append(token)
                            self.symbol_table[0].append(token_type)
                            self.symbol_table[0].append('0' + str(self.current_mem_space))
                            self.current_row_index += 1
                            self.current_mem_space += 1
                    else:
                        return 'Fatal Error: Out of Memory.'

        print 'Symbol Table:' 
        for symbol in self.symbol_table: print symbol

    def get_labels(self):
        for token, token_type in self.token_dictionary.iteritems():
            if token_type == 'label':
                if self.current_row_index != 0:
                    if not token in (li[0] for li in self.symbol_table):
                        if self.current_mem_space < 10:
                            row = []
                            row.append(token[:-1])
                            row.append(token_type)
                            row.append('0' + str(self.current_mem_space))
                            self.symbol_table.append(row)
                            self.current_row_index += 1
                            self.current_mem_space += 1
                        else:
                            return 'Fatal Error: Out of Memory.'
                else:
                    if self.current_mem_space < 10:
                            self.symbol_table[0].append(token[:-1])
                            self.symbol_table[0].append(token_type)
                            self.symbol_table[0].append('0' + str(self.current_mem_space))
                            self.current_row_index += 1
                            self.current_mem_space += 1
                    else:
                        return 'Fatal Error: Out of Memory.'
