from lexer import tokenize
from parser import parse
from compiler import compile_ast
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <source.plang>")
        return
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        code = f.read()

    tokens = tokenize(code)
    ast = parse(tokens)
    output = compile_ast(ast)

    print("🔊 PulseLang Output:")
    print(output)

if __name__ == "__main__":
    main()
