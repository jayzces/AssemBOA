import string, re
from collections import defaultdict

class SemanticAnalyzer(object):
    def __init__(self, token_dictionary):
        super(SemanticAnalyzer, self).__init__()
        self.token_dictionary = token_dictionary
        self.symbol_table = defaultdict(list)
        self.current_row_index = 0
        self.current_mem_space = 0
        self.num_of_errors = 0
        self.errors = {
            'Missing BEGIN Error': 'Missing BEGIN Error: "BEGIN" command not found at line 1.',
            'Misplaced BEGIN Error': 'Misplaced BEGIN Error: More than one instance of "BEGIN" command found.',
            'OutOfMem': 'Fatal Error: Out of Memory.'
        }

    def analyze(self, filename):
        is_begin_found = False
        line_number = 1

        with open(filename, "r") as txt:
            for line in txt:
                line = str(line.strip())
                # print line
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
                                self.num_of_errors += 1
                        else:
                            if tokens[x] == 'begin' or tokens[x] == 'BEGIN':
                                if is_begin_found:
                                    print self.errors['Misplaced BEGIN Error']
                                    self.num_of_errors += 1
                            elif tokens[x] == 'end' or tokens[x] == 'END':
                                break
                                print line_number
                else:
                    if line_number == 1:
                        if line == 'begin' or line == 'BEGIN':
                            is_begin_found = True
                        else:
                            print self.errors['Missing BEGIN Error']
                            self.num_of_errors += 1
                    else:
                        if line == 'begin' or line == 'BEGIN':
                            if is_begin_found:
                                print self.errors['Misplaced BEGIN Error']
                                self.num_of_errors += 1
                        elif line == 'end' or line == 'END':
                            break
                            print line_number
                line_number += 1



        if self.num_of_errors == 0:
            print '\nSemantic Analysis Complete. No errors found.\n'
        else:
            if self.num_of_errors > 1:
                print '\nSemantic Analysis Complete. ' + str(self.num_of_errors) + ' errors were found.\n'
            else:
                print '\nSemantic Analysis Complete. ' + str(self.num_of_errors) + ' error was found.\n'

        self.generate_symbol_table()

    def generate_symbol_table(self):
        # place labels in the symbol_table first
        self.get_labels()
        for item in self.token_dictionary:
            if item[1] == 'identifier':
                if self.current_mem_space < 10:
                    if not item[0] in self.symbol_table:
                        if self.current_mem_space < 10:
                            self.symbol_table[item[0]].append(item[1])
                            self.symbol_table[item[0]].append('0' + str(self.current_mem_space))
                            self.current_row_index += 1
                            self.current_mem_space += 1
                else:
                    print self.errors['OutOfMem']
                    self.num_of_errors += 1
                    return

        print 'Symbol Table:' 
        for key in self.symbol_table.iterkeys(): print "[%s: %s]" % (key, self.symbol_table[key])

    def get_labels(self):
        for item in self.token_dictionary:
            if item[1] == 'label':
                if self.current_mem_space < 10:
                    if not item[0][:-1] in self.symbol_table:
                        if self.current_mem_space < 10:
                            self.symbol_table[item[0][:-1]].append(item[1])
                            self.symbol_table[item[0][:-1]].append('0' + str(self.current_mem_space))
                            self.current_row_index += 1
                            self.current_mem_space += 1
                else:
                    print self.errors['OutOfMem']
                    self.num_of_errors += 1
                    return
