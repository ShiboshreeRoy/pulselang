def parse(tokens):
    ast = []
    i = 0
    while i < len(tokens):
        token_type, token_value = tokens[i]
        if token_type == 'COMMAND' and tokens[i+1][0] == 'STRING':
            ast.append(('SAY', tokens[i+1][1][1:-1]))  # Remove quotes
            i += 2
        elif token_type == 'NEWLINE':
            i += 1
        else:
            raise SyntaxError(f"Unexpected token: {token_type}")
    return ast
