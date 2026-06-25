import ply.yacc as yacc
from src.roman_lexer import tokens, lexer as _roman_lexer

# Exponer el lexer para que PLY use el lexer correcto al parsear
lexer = _roman_lexer

# Gramática G2 (right-recursive for Low*):

def p_romanNumber(p):
    """romanNumber : thousand hundred ten digit"""
    vals = [p[1]["val"], p[2]["val"], p[3]["val"], p[4]["val"]]
    valids = [p[1]["valid"], p[2]["valid"], p[3]["valid"], p[4]["valid"]]
    if all(valids):
        p[0] = {"valid": True, "val": sum(vals)}
    else:
        p[0] = {"valid": False, "val": -1}


def p_thousand(p):
    """thousand : M M M
                | M M
                | M
                | lambda"""
    if len(p) == 4:
        p[0] = {"valid": True, "val": 3000}
    elif len(p) == 3:
        p[0] = {"valid": True, "val": 2000}
    elif len(p) == 2:
        if p[1] is None:
            p[0] = {"valid": True, "val": 0}
        else:
            p[0] = {"valid": True, "val": 1000}
    else:
        p[0] = {"valid": True, "val": 0}


# LowHundreds (right-recursive): low_hundreds -> C low_hundreds | lambda
def p_low_hundreds_rec(p):
    """low_hundreds : C low_hundreds"""
    right = p[2]
    if not right["valid"]:
        p[0] = {"valid": False, "val": -1, "count": right.get("count", 0)}
    else:
        cnt = right.get("count", 0) + 1
        if cnt > 3:
            p[0] = {"valid": False, "val": -1, "count": cnt}
        else:
            p[0] = {"valid": True, "val": right.get("val", 0) + 100, "count": cnt}


def p_low_hundreds_empty(p):
    """low_hundreds : lambda"""
    p[0] = {"valid": True, "val": 0, "count": 0}


def p_small_hundred(p):
    """small_hundred : C C C
                      | C C
                      | C"""
    if len(p) == 4:
        p[0] = {"valid": True, "val": 300}
    elif len(p) == 3:
        p[0] = {"valid": True, "val": 200}
    else:
        p[0] = {"valid": True, "val": 100}


def p_hundred(p):
    """hundred : low_hundreds
               | C M
               | C D
               | D low_hundreds
               | lambda"""
    if len(p) == 2 and isinstance(p[1], dict):
        p[0] = {"valid": p[1]["valid"], "val": p[1]["val"]}
    elif len(p) == 3 and p[1] == 'C' and p[2] == 'M':
        p[0] = {"valid": True, "val": 900}
    elif len(p) == 3 and p[1] == 'C' and p[2] == 'D':
        p[0] = {"valid": True, "val": 400}
    elif len(p) == 3 and p[1] == 'D':
        p[0] = {"valid": True, "val": 500 + p[2]["val"]}
    else:
        p[0] = {"valid": True, "val": 0}


# LowTens (right-recursive): low_tens -> X low_tens | lambda
def p_low_tens_rec(p):
    """low_tens : X low_tens"""
    right = p[2]
    if not right["valid"]:
        p[0] = {"valid": False, "val": -1, "count": right.get("count", 0)}
    else:
        cnt = right.get("count", 0) + 1
        if cnt > 3:
            p[0] = {"valid": False, "val": -1, "count": cnt}
        else:
            p[0] = {"valid": True, "val": right.get("val", 0) + 10, "count": cnt}


def p_low_tens_empty(p):
    """low_tens : lambda"""
    p[0] = {"valid": True, "val": 0, "count": 0}


def p_small_ten(p):
    """small_ten : X X X
                 | X X
                 | X"""
    if len(p) == 4:
        p[0] = {"valid": True, "val": 30}
    elif len(p) == 3:
        p[0] = {"valid": True, "val": 20}
    else:
        p[0] = {"valid": True, "val": 10}


def p_ten(p):
    """ten : low_tens
           | X C
           | X L
           | L low_tens
           | lambda"""
    if len(p) == 2 and isinstance(p[1], dict):
        p[0] = {"valid": p[1]["valid"], "val": p[1]["val"]}
    elif len(p) == 3 and p[1] == 'X' and p[2] == 'C':
        p[0] = {"valid": True, "val": 90}
    elif len(p) == 3 and p[1] == 'X' and p[2] == 'L':
        p[0] = {"valid": True, "val": 40}
    elif len(p) == 3 and p[1] == 'L':
        p[0] = {"valid": True, "val": 50 + p[2]["val"]}
    else:
        p[0] = {"valid": True, "val": 0}


# LowUnits (right-recursive): low_units -> I low_units | lambda
def p_low_units_rec(p):
    """low_units : I low_units"""
    right = p[2]
    if not right["valid"]:
        p[0] = {"valid": False, "val": -1, "count": right.get("count", 0)}
    else:
        cnt = right.get("count", 0) + 1
        if cnt > 3:
            p[0] = {"valid": False, "val": -1, "count": cnt}
        else:
            p[0] = {"valid": True, "val": right.get("val", 0) + 1, "count": cnt}


def p_low_units_empty(p):
    """low_units : lambda"""
    p[0] = {"valid": True, "val": 0, "count": 0}


def p_small_digit(p):
    """small_digit : I I I
                   | I I
                   | I"""
    if len(p) == 4:
        p[0] = {"valid": True, "val": 3}
    elif len(p) == 3:
        p[0] = {"valid": True, "val": 2}
    else:
        p[0] = {"valid": True, "val": 1}


def p_digit(p):
    """digit : low_units
             | I X
             | I V
             | V low_units
             | lambda"""
    if len(p) == 2 and isinstance(p[1], dict):
        p[0] = {"valid": p[1]["valid"], "val": p[1]["val"]}
    elif len(p) == 3 and p[1] == 'I' and p[2] == 'X':
        p[0] = {"valid": True, "val": 9}
    elif len(p) == 3 and p[1] == 'I' and p[2] == 'V':
        p[0] = {"valid": True, "val": 4}
    elif len(p) == 3 and p[1] == 'V':
        p[0] = {"valid": True, "val": 5 + p[2]["val"]}
    else:
        p[0] = {"valid": True, "val": 0}


# Definir lambda
def p_empty(p):
    'lambda :'
    pass


def p_roman(p):
    """roman : romanNumber"""
    p[0] = p[1]


def p_error(p):
    raise Exception("Error de sintaxis en '%s'" % p.value if p else "EOF")


# Construir el parser
parser = yacc.yacc()

# Forcer parse to use the correct lexer instance
_original_parse = parser.parse
def _parse_with_lexer(input_string, debug=False):
    return _original_parse(input_string, lexer=_roman_lexer, debug=debug)
parser.parse = _parse_with_lexer


if __name__ == "__main__":
    while True:
        try:
            s = input("Ingrese un número romano: ")
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(f"El valor numérico es: {result}")


