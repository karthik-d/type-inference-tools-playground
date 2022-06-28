# src/graph_transpiler/webdnn/graph/shape.py

def parse(text):
    normalized_text = _normalize_text(text)
    tmp = ast.literal_eval(normalized_text)
    shape = []
    placeholders = {}
    for i , t in enumerate(tmp) :
        if isinstance(t, str) :
            pt = Placeholder(label=t)
            placeholders [t] = pt
        elif isinstance (t, int) :
            pt = t
        shape.append(pt)
    return shape, placeholders