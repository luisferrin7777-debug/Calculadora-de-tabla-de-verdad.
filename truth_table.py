import itertools
import re

def extract_variables(expression):
    # Extrae variables (letras mayúsculas)
    variables = sorted(set(re.findall(r'\b[A-Z]\b', expression)))
    return variables

def safe_eval(expr, values):
    # Reemplazar operadores por equivalentes en Python
    expr = expr.replace("AND", "and")
    expr = expr.replace("OR", "or")
    expr = expr.replace("NOT", "not")
    expr = expr.replace("XOR", "^")

    # Reemplazar variables con valores (0/1)
    for var, val in values.items():
        expr = re.sub(rf'\b{var}\b', str(bool(val)), expr)

    # Evaluar expresión de forma controlada
    result = eval(expr, {"__builtins__": None}, {})

    return int(result)

def generate_truth_table(expression):
    variables = extract_variables(expression)

    if not variables:
        raise ValueError("No se encontraron variables válidas (A, B, C...)")

    combinations = list(itertools.product([0, 1], repeat=len(variables)))

    table = []

    for combo in combinations:
        values = dict(zip(variables, combo))
        result = safe_eval(expression, values)
        row = list(combo) + [result]
        table.append(row)

    return variables, table