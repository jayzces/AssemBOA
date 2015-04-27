import string, re

class SemanticAnalyzer(object):
    def __init__(self, token_dictionary):
        super(SemanticAnalyzer, self).__init__()
        self.token_dictionary = token_dictionary
        self.symbol_table = [[]]
        self.current_row_index = 0
        self.current_mem_space = 0
        self.errors = {
            'Missing BEGIN Error': 'Missing BEGIN Error: "BEGIN" command not found at line 1.',
            'Misplaced BEGIN Error': 'Misplaced BEGIN Error: More than one instance of "BEGIN" command found.',
        }

    def analyze(self, filename):
        is_begin_found = False
        line_number = 1

        with open(filename, "r") as txt:
            for line in txt:
                line = str(line.strip())
                print line
                if re.search(r"\s", line):
                # if ' ' in line:
                    tokens = line.split()
                    for x in range(0, len(tokens)):
                        if x == 0 and line_number == 1:
                            if tokens[x] == 'begin' or tokens[x] == 'BEGIN':
                                is_begin_found = True
                            else:
                                print tokens[x]
                                print self.errors['Missing BEGIN Error']
                        else:
                            if tokens[x] == 'begin' or tokens[x] == 'BEGIN':
                                if is_begin_found:
                                    print self.errors['Misplaced BEGIN Error']
                            elif tokens[x] == 'end' or tokens[x] == 'END':
                                break
                                print line_number
                else:
                    if line_number == 1:
                        if line == 'begin' or line == 'BEGIN':
                            is_begin_found = True
                        else:
                            print self.errors['Missing BEGIN Error']
                    else:
                        if line == 'begin' or line == 'BEGIN':
                            if is_begin_found:
                                print self.errors['Misplaced BEGIN Error']
                        elif line == 'end' or line == 'END':
                            break
                            print line_number
                line_number += 1

    def generate_symbol_table(self):
        # place labels in the symbol_table first
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
