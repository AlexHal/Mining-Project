from evaluate_expr import evaluate_expr
def index_getter(values):
    snapshot = list(values)
    def get(idx):
        i = int(float(idx)) - 1
        if i < 0 or i >= len(snapshot):
            raise IndexError(f"Index {idx} out of range (len={len(snapshot)})")
        # print(snapshot[i])
        return snapshot[i]
    return get


def get_matrix_expr(matrix: dict, row_label: str, column_key: str, default: str = "") -> str:
    row = matrix[str(row_label[:-6])]
    
    key = str(column_key).strip()
    
    idx = int(float(key))
    ordered_keys = list(row.keys())
    
    expr = row.get(ordered_keys[idx - 1], default)
    return str(expr)



