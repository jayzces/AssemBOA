import string

def lex_check(filename, symbol_table):
    with open(filename, "r") as txt:
        for line in txt:
            is_correct = lex_analyze(line.strip(), symbol_table)
            if not is_correct:
                return False

    return True

def lex_analyze(line, symbol_table):
    tokens = line.split()

    if len(tokens) == 1:
        if not lex_is_command(tokens[0], symbol_table) and not lex_is_macro(tokens[0], symbol_table):
            return False
    elif len(tokens) == 2:
        if lex_is_command(tokens[0], symbol_table):
            if tokens[0] == 'pushi':
                if int(tokens[1]) < 0 or int(tokens[1]) > 99:
                    return False
            else:
                if not lex_is_identifier(tokens[1], symbol_table):
                    return False
        else:
            return False

    return True


def lex_is_command(token, symbol_table):
    return symbol_table.has_key(token.lower())


def lex_is_identifier(token, symbol_table):
    if token not in string.digits and token.isalpha() and not symbol_table.has_key(token.lower()):
        for c in token:
            if c.isalnum() or c == '_':
                continue
            else:
                return False
        return True
    else:
        return False


# because vincent said so
def lex_is_macro(token, symbol_table):
    s = token[:-1]
    c = token[-1]

    return lex_is_identifier(s, symbol_table) and c == ':'