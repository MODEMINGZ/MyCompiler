import sys
from .lexer.scanner import tokenize
from .parser.parser import parse
from .exceptions import CillyError


def main():
    if len(sys.argv) != 2:
        print("Usage: python -m cilly <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, "r") as file:
            source = file.read()

        tokens = tokenize(source)
        ast = parse(tokens)

        print("Tokens:")
        for token in tokens:
            print(token)

        print("\nAbstract Syntax Tree:")
        print_ast(ast)

    except CillyError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)


def print_ast(node, indent=""):
    if isinstance(node, list):
        print(f"{indent}{node[0]}")
        for child in node[1:]:
            print_ast(child, indent + "  ")
    else:
        print(f"{indent}{node}")


if __name__ == "__main__":
    main()
