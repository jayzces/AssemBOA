from lex import *

class Assemboa(object):
    symbol_table = {
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

    variable_address = {}

    def analyze(self, file_to_read):
        if lex_check(file_to_read, self.symbol_table):
            print 'Lexical Analysis Complete. No error found.'
        else:
            print 'PATAKA LANG! BOGO HAHAHAHAHAHAHA'


    # def read_and_write(self, file_to_read, file_to_write_to):
    #     f = open(file_to_read, 'rb')
    #     nf = open(file_to_write_to, 'wb')
    #     for line in f:
    #         translated_line = self.translate(line)
    #         nf.write(translated_line + '\n')

    #         if translated_line == 'error':
    #             break

    #     nf.close()

            
    # def translate(self, line):
    #     tokens = line.strip().split()
    #     translated = ''
    #     command = '' # keep track of previous command for pushi

    #     if len(tokens) == 1:
    #         token_lowercase = tokens[0].lower()
    #         if symbol_table.has_key(token_lowercase):
    #             translated += symbol_table.get(token_lowercase)
    #         else:
    #             translated = 'error'
    #             return translated
    #     elif len(tokens) == 2:
    #         token_lowercase = tokens[0].lower()
    #         if symbol_table.has_key(token_lowercase):
    #             translated += symbol_table.get(token_lowercase)
    #         else:
    #             translated = 'error'
    #             return translated

    #         if self.is_identifier(tokens[1]):
    #             if variable_address.has_key(tokens[1]):
    #                 translated += variable_address.get(tokens[1])
    #             else:
    #                 if len(variable_address) < 10:
    #                     current_address = '0' +  str(len(variable_address) + 1)
    #                     variable_address[tokens[1]] = current_address
    #                     translated += current_address
    #                 else:
    #                     translated = 'error'
    #         elif int(tokens[1]) > 0:
    #             if command == 'pushi':
    #                 if len(tokens[1]) < 2:
    #                     translated += '0' + tokens[1]
    #                 else:
    #                     translated += tokens[1]
    #             else:
    #                 translated = 'error'
    #         else:
    #             translated = 'error'
                
    #     return translated


    # def is_identifier(self, token):

    #     if token[0] not in string.digits and token[0].isalpha() and not symbol_table.has_key(token.lower()):
    #         for c in token:
    #             if c.isalnum() or c == '_':
    #                 continue
    #             else:
    #                 return False

    #         return True
    #     else:
    #         return False
