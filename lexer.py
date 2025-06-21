import re

TOKEN_TYPES = [
    ('STRING', r'"[^"]*"'),
    ('COMMAND', r'say'),
    ('NEWLINE', r'\n'),
    ('WHITESPACE', r'[ \t]+'),
]

def tokenize(code):
    tokens = []
    i = 0
    while i < len(code):
        match = None
        for token_type, pattern in TOKEN_TYPES:
            regex = re.compile(pattern)
            match = regex.match(code, i)
            if match:
                if token_type != 'WHITESPACE':
                    tokens.append((token_type, match.group()))
                i = match.end()
                break
        if not match:
            raise SyntaxError(f"Unexpected character: {code[i]}")
    return tokens
