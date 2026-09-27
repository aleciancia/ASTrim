# ASTrim: AST-Driven Context Pruner for LLMs

#### Description:
When interacting with Large Language Models (LLMs) for code generation or debugging, context window limits and token costs are primary bottlenecks. Passing entire raw source files to a model often wastes tokens on internal implementation details (e.g., loops, database connection logic, private helper methods) that the LLM does not need in order to understand the system's architecture or write caller code.

ASTrim is a command-line tool that acts as a syntactic surgeon. Instead of relying on fragile Regular Expressions, it parses Python source code into its native Abstract Syntax Tree (AST). It traverses the tree and prunes the bodies of functions and methods, replacing them with syntactically valid `...` (Ellipses), while perfectly preserving class structures, type hints, function signatures, and docstrings.

The result is a stripped-down, syntactically valid skeleton of the codebase that drastically reduces token consumption (often by 50-70%) while providing the LLM with 100% of the API contracts it needs to interact with the code.

## How It Works (Under the Hood)

The core logic relies on Python's built-in `ast` module. 
1. The source code is parsed into a node tree.
2. A custom `ast.NodeTransformer` class (`ASTPruner`) visits every `FunctionDef` and `AsyncFunctionDef` node.
3. If a docstring is present (`ast.get_docstring`), it is preserved as the first element of the new body.
4. The rest of the implementation is discarded and replaced by an `ast.Expr` containing an `ast.Constant(Ellipsis)`.
5. The manipulated tree is unparsed back into standard Python source code.
6. The token reduction is calculated using OpenAI's `tiktoken` library (using the `cl100k_base` encoding) to provide an accurate real-world metric rather than naive word counting.

## Project Structure

- `project.py`: The main entry point containing the CLI logic, the `ASTPruner` class, and the core functions required by the CS50P specification (`parse_arguments`, `prune_source_code`, `calculate_token_reduction`).
- `test_project.py`: A comprehensive `pytest` suite covering edge cases, syntax errors, and validation of token reduction math.
- `requirements.txt`: Project dependencies (`pytest`, `tiktoken`).
- `examples/sample.py`: A dummy ETL data pipeline file used to test and demonstrate the pruning capabilities.

## Design Choices

I explicitly chose an AST-based approach over Regex. Regular expressions are notoriously brittle when dealing with nested brackets, multiline strings, or unconventional indentation in Python. By leveraging the compiler's own parser, ASTrim guarantees that the output will never suffer from an `IndentationError` or a missing closing parenthesis. If the input code is valid Python, the output skeleton is guaranteed to be valid Python. 

The tool was designed to be modular. The parsing, pruning, and token calculation steps are decoupled, making it straightforward to integrate `prune_source_code()` as a pre-processing step in automated CI/CD pipelines or RAG (Retrieval-Augmented Generation) architectures.

## Usage

Install dependencies:
```bash
pip install -r requirements.txt