PULSE_MAP = {
    'A': '^~', 'B': '~^^^', 'C': '~^~^', 'D': '~^^', 'E': '^',
    'F': '^^~^', 'G': '~~^', 'H': '^^^', 'I': '~^', 'J': '^~~~',
    'K': '~^~', 'L': '^~^^', 'M': '~~', 'N': '~^', 'O': '~~~',
    'P': '^~~^', 'Q': '~~^~', 'R': '^~^', 'S': '^^^', 'T': '~',
    'U': '^^~', 'V': '^^^~', 'W': '^~~', 'X': '~^^~', 'Y': '~^~~',
    'Z': '~~^^', '1': '^~***', '2': '^^~**', '3': '^^^~*',
    '4': '^^^^~', '5': '~~~~^', ' ': '_'
}

def encode_to_pulse(text):
    return '_'.join(PULSE_MAP.get(c.upper(), '?') for c in text)

def compile_ast(ast):
    output = []
    for command, value in ast:
        if command == 'SAY':
            encoded = encode_to_pulse(value)
            output.append(f'[{encoded}]')
    return '\n'.join(output)
