import string

class SyntacticAnalyzer(object):
    def __init__(self):
        super(SyntacticAnalyzer, self).__init__()
        command_list = {
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
        self.errors = {
            'Unknown Command': 'Error: Unknown Command: ',
            'Overflow': 'Overflow Error: Argument or result is lesser than 0 or greater than 99.',
            'Identifier Expected': 'Error: Identifier expected. '
        }


    def analyze(self, file_to_read):
        if syntax_check(file_to_read, self.command_list):
            print 'Syntactic Analysis Complete. No errors found.'
        else:
            print 'PATAKA LANG! BOGO HAHAHAHAHAHAHA'

    def syntax_check(filename, command_list):
        with open(filename, "r") as txt:
            for line in txt:
                is_correct = syntax_analyze(line.strip(), command_list)
                if not is_correct:
                    return False

        return True

    def syntax_analyze(line, command_list):
        tokens = line.split()

        if len(tokens) == 1:
            if not is_command(tokens[0], command_list) and not is_macro(tokens[0], command_list):
                print self.errors['Unknown Command'] + tokens[0]
        elif len(tokens) == 2:
            if is_command(tokens[0], command_list):
                if tokens[0] == 'pushi':
                    if int(tokens[1]) < 0 or int(tokens[1]) > 99:
                        print self.errors['Overflow']
                else:
                    if not is_identifier(tokens[1], command_list):
                        print self.errors['Identifier Expected']
            else:
                print self.errors['Unknown Command'] + tokens[0]

        return True


    def is_command(token, command_list):
        return command_list.has_key(token.lower())


    def is_identifier(token, command_list):
        if token not in string.digits and token.isalpha() and not command_list.has_key(token.lower()):
            for c in token:
                if c.isalnum() or c == '_':
                    continue
                else:
                    return False
            return True
        else:
            return False

    def is_macro(token, command_list):
        s = token[:-1]
        c = token[-1]

        return is_identifier(s, command_list) and c == ':'
