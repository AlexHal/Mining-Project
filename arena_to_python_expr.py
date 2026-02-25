#  so we have && || <> to purge and replace
def arena_to_python_expr(expr : str) -> str:
    expr = expr.strip()

    # expr are stored in " " hence we must remove them
    if len(expr) >= 2 and expr[0] == '"' and expr[-1] == '"':
        expr = expr[1:-1] # remove first and last arg


    expr = expr.replace("&&", "and")
    expr = expr.replace("||", "or")
    expr = expr.replace("<>", "!=")


    return expr