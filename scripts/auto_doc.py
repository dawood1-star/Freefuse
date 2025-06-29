import ast
import sys
from typing import Any

class DocstringAdder(ast.NodeTransformer):
    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.generic_visit(node)
        if ast.get_docstring(node):
            return node
        params = [arg.arg for arg in node.args.args if arg.arg != "self"]
        lines = [f"{node.name} function.", "", "Parameters:"]
        if params:
            lines.extend([f"    {p} (Any): TODO." for p in params])
        else:
            lines.append("    None")
        lines.extend(["", "Returns:", "    TODO."])
        docstring = "\n".join(lines)
        node.body.insert(0, ast.Expr(value=ast.Constant(docstring)))
        return node

def add_docstrings(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
    tree = DocstringAdder().visit(tree)
    ast.fix_missing_locations(tree)
    code = ast.unparse(tree)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python auto_doc.py <python_file>")
        sys.exit(1)
    add_docstrings(sys.argv[1])
