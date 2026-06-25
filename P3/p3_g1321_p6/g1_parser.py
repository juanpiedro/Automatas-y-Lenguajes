import ply.yacc as yacc
from src.g1_lexer import tokens, lexer as _g1_lexer

# Exponer el lexer para que PLY use el lexer correcto al parsear
lexer = _g1_lexer

# Gramática


def p_Language(p):
    """Language : A B C"""
    a = p[1]["a"]
    b = p[2]["b"]
    c = p[3]["c"]
    # Acepta cuando número de b == número de a y número de c == número de a + 1
    p[0] = (a == b and c == a + 1)

def p_A(p):
    """A : a A
        | lambda"""
    if len(p) == 3:
        p[0] = {"a": 1 + p[2]["a"]}
    else:
        p[0] = {"a": 0}
def p_B(p):
    """B : b B
        | lambda"""
    if len(p) == 3:
        p[0] = {"b": 1 + p[2]["b"]}
    else:
        p[0] = {"b": 0}

def p_C(p):
    """C : c C
        | lambda"""
    if len(p) == 3:
        p[0] = {"c": 1 + p[2]["c"]}
    else:
        p[0] = {"c": 0}

def p_lambda(p):
    """lambda :"""
    pass  # Producción vacía

# Manejo de errores sintácticos
def p_error(p):
    print("Error de sintaxis en '%s'" % p.value if p else "EOF")

# Construir el parser
parser = yacc.yacc()

# Forcer parse to use the correct lexer instance (evitar ambigüedades entre lexers)
_original_parse = parser.parse
def _parse_with_lexer(input_string, debug=False):
    return _original_parse(input_string, lexer=_g1_lexer, debug=debug)
parser.parse = _parse_with_lexer

if __name__ == "__main__":
    while True:
        try:
            s = input("Ingrese una cadena: ")
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(f"El valor numérico es:", result)

