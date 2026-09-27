import argparse
import ast
import sys
import tiktoken

class ASTPruner(ast.NodeTransformer):
    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        self.generic_visit(node)
        return self._prune_body(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AsyncFunctionDef:
        self.generic_visit(node)
        return self._prune_body(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        self.generic_visit(node)
        return node

    def _prune_body(self, node):
        new_body = []
        if ast.get_docstring(node):
            new_body.append(node.body[0])
        new_body.append(ast.Expr(value=ast.Constant(value=...)))
        node.body = new_body
        return node
        

def main():
    args = parse_arguments()
    
    try:
        with open(args.filepath, "r", encoding="utf-8") as f:
            original_code = f.read()
    except FileNotFoundError:
        sys.exit(f"Errore: il file {args.filepath} non esiste.")

    try:
        pruned_code = prune_source_code(original_code)
    except SyntaxError:
        sys.exit("Errore: il file fornito non contiene codice Python sintatticamente valido.")

    reduction = calculate_token_reduction(original_code, pruned_code)

    print(pruned_code)
    print("\n" + "="*40)
    print(f"Token reduction: {reduction}%")
    print("="*40 + "\n")

def parse_arguments(args: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", type=str)
    return parser.parse_args(args)

def prune_source_code(source_code: str) -> str:
    tree = ast.parse(source_code)
    pruner = ASTPruner()
    pruned_tree = pruner.visit(tree)
    ast.fix_missing_locations(pruned_tree)
    return ast.unparse(pruned_tree)

def calculate_token_reduction(original_text: str, pruned_text: str) -> float:
    enc = tiktoken.get_encoding("cl100k_base")
    orig_tokens = len(enc.encode(original_text))
    pruned_tokens = len(enc.encode(pruned_text))
    
    if orig_tokens == 0:
        return 0.0
        
    reduction = ((orig_tokens - pruned_tokens) / orig_tokens) * 100
    return round(reduction, 2)

if __name__ == "__main__":
    main()