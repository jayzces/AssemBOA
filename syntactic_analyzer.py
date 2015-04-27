import string
from collections import OrderedDict

class SyntacticAnalyzer(object):
    def __init__(self):
        super(SyntacticAnalyzer, self).__init__()
        self.command_list = {
            'begin': '0000',
            'read': '01',
            'disp': '02',
            'pushi': '03',
            'pushv': '04',
            'pop': '05',
            'mod': '0600',
            'jmp': '07',
            'jl': '08',
            'jg': '09',
            'jeq': '10',
            'add': '1100',
            'sub': '1200',
            'cmp': '1300',
            'end': '9999',
        }        
        self.num_of_errors = 0
        self.errors = {
            'Unknown Command': 'Error: Unknown command ',
            'Overflow': 'Overflow Error: Argument or result is lesser than 0 or greater than 99.',
            'Identifier Expected': 'Error: Identifier expected ',
            'Integer Value Expected' : 'Error: Integer value expected ',
        }
        self.token_dictionary = OrderedDict()

    def syntax_check(self, filename):
        with open(filename, "r") as txt:
            line_number = 0
            for line in txt:
                line_number += 1
                is_correct = self.syntax_analyze(line.strip(), line_number)
                if not is_correct:
                    return False

        return True

    def syntax_analyze(self, line, line_number):
        tokens = line.split()

        if len(tokens) == 1:
            if not self.is_command(tokens[0]) and not self.is_label(tokens[0]):
                self.num_of_errors += 1
                print self.errors['Unknown Command'] + 'at line ' + str(line_number) + ': ' + ' "' + tokens[0] + '"'
        elif len(tokens) == 2:
            if self.is_command(tokens[0]):
                if tokens[0] == 'pushi':
                    try:
                        integer = int(tokens[1])
                        if int(tokens[1]) < 0 or int(tokens[1]) > 99:
                            self.num_of_errors += 1
                            print self.errors['Overflow']
                    except ValueError:
                        self.num_of_errors += 1
                        print self.errors['Integer Value Expected'] + 'at line ' + str(line_number) + ': "' + tokens[1] + '" found.'
                elif tokens[0] == 'begin' or tokens[0] == 'end' or tokens[0] == 'add' or tokens[0] == 'sub' or tokens[0] == 'mod' or tokens[0] == 'cmp':                   
                    self.num_of_errors += 1                    
                    print self.errors['Unknown Command'] + 'at line ' + str(line_number) + ': ' + ' "' + tokens[1] + '"'
                else:
                    if not self.is_identifier(tokens[1]):
                        self.num_of_errors += 1
                        print self.errors['Identifier Expected'] + 'at line ' + str(line_number) + ': "' + tokens[1] + '" found.'
            else:
                self.num_of_errors += 1
                print self.errors['Unknown Command'] + 'at line ' + str(line_number) + ': ' + ' "' + tokens[0] + '"'
        # error-handling for lines with more than two tokens
        elif len(tokens) > 2:
            # if line starts with an identifier
            if self.is_identifier(tokens[0]):
                self.num_of_errors += len(tokens)
                for token in tokens:
                    print self.errors['Unknown Command'] + 'at line ' + str(line_number) + ': "' + token + '"'
            # if line starts with a command
            elif self.is_command(tokens[0]):
                if tokens[0] == 'pushi':
                    try:
                        integer = int(tokens[1])
                        if int(tokens[1]) < 0 or int(tokens[1]) > 99:
                            self.num_of_errors += 1
                            print self.errors['Overflow']
                    except ValueError:
                        self.num_of_errors += 1
                        print self.errors['Integer Value Expected'] + 'at line ' + str(line_number) + ': "' + tokens[1] + '" found.'
                    for x in range(1, len(tokens)):                        
                        self.num_of_errors += 1
                        print self.errors['Unknown Command'] + 'at line ' + str(line_number) + ': "' + tokens[x] + '"'
                # if command does not require parameters and parameters are found
                elif tokens[0] == 'begin' or tokens[0] == 'end' or tokens[0] == 'add' or tokens[0] == 'sub' or tokens[0] == 'mod' or tokens[0] == 'cmp':
                    for x in range(1, len(tokens)):
                        self.num_of_errors += 1
                        print self.errors['Unknown Command'] + 'at line ' + str(line_number) + ': "' + tokens[x] + '"'
                # if second token is not an identifier
                elif not self.is_identifier(tokens[1]):
                    for x in range(1, len(tokens)):
                        self.num_of_errors += 1
                        print self.errors['Unknown Command'] + 'at line ' + str(line_number) + ': "' + tokens[x] + '"'
                elif self.is_identifier(tokens[1]):
                    for x in range(2, len(tokens)):
                        self.num_of_errors += 1
                        print self.errors['Unknown Command'] + 'at line ' + str(line_number) + ': "' + tokens[x] + '"'
                else:
                    for token in tokens:
                        self.num_of_errors += 1
                        print self.errors['Unknown Command'] + 'at line ' + str(line_number) + ': "' + token + '"'
            else:
                for token in tokens:
                    self.num_of_errors += 1
                    print self.errors['Unknown Command'] + 'at line ' + str(line_number) + ': "' + token + '"'
        return True


    def is_command(self, token):
        return self.command_list.has_key(token.lower())


    def is_identifier(self, token):
        if token not in string.digits and token.isalpha() and not self.command_list.has_key(token.lower()):
            for c in token:
                if c.isalnum() or c == '_':
                    continue
                else:
                    return False
            return True
        else:
            return False

    def is_label(self, token):
        s = token[:-1]
        c = token[-1]

        return self.is_identifier(s) and c == ':'

    def analyze(self, file_to_read):
        self.syntax_check(file_to_read)

        if self.num_of_errors == 0:
            print 'Syntactic Analysis Complete. No errors found.'
        else:
            if self.num_of_errors > 1:
                print 'Syntactic Analysis Complete. ' + str(self.num_of_errors) + ' errors were found.'
            else:
                print 'Syntactic Analysis Complete. ' + str(self.num_of_errors) + ' error was found.'

    def get_token_dictionary(self, filename):
         with open(filename, "r") as txt:
            for line in txt:
                line = line.strip()
                tokens = line.split()
                for token in tokens:
                    if self.is_identifier(token):
                        self.token_dictionary[token] = 'identifier'
                    elif self.is_command(token):
                        self.token_dictionary[token] = 'command'
                    elif self.is_label(token):
                        self.token_dictionary[token] = 'label'
                    else:
                        try:
                            integer = int(tokens[1])
                            self.token_dictionary[token] = 'integer'
                        except ValueError:
                            self.token_dictionary[token] = 'identifier'