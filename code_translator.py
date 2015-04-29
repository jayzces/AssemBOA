class CodeTranslator(object):
    def __init__(self, tokens, symbol_table):
        super(CodeTranslator, self).__init__()
        self.label_code = '69'
        self.tokens = tokens
        self.symbol_table = symbol_table
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
    
    def translate(self, output_filename):
        output = open(output_filename, 'wb')
        for idx, token in enumerate(self.tokens):
            if token[0] in self.command_list:
                output.write(self.command_list[token[0]])

                if len(self.command_list[token[0]]) >= 4 and idx < len(self.tokens) - 1:
                    output.write('\n')
            elif token[1] == 'integer':
                output.write(token[0].zfill(2))
                if idx < len(self.tokens) - 1:
                    output.write('\n')
            elif token[1] == 'identifier':
                output.write(self.symbol_table.get(token[0])[1])
                if idx < len(self.tokens) - 1:
                    output.write('\n')
            elif token[1] == 'label':
                output.write(self.label_code + self.symbol_table.get(token[0][:-1])[1])
                if idx < len(self.tokens) - 1:
                    output.write('\n')

        print '\nTranslation complete. Machine code is stored in file "' + output_filename + '".\n'
