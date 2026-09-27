import pytest
from project import parse_arguments, prune_source_code, calculate_token_reduction

def test_parse_arguments():
    args = parse_arguments(["test_file.py"])
    assert args.filepath == "test_file.py"

    with pytest.raises(SystemExit):
        parse_arguments([])

def test_prune_source_code():
    original_code = """
def sum_numbers(a: int, b: int) -> int:
    \"\"\"Returns the sum of two numbers.\"\"\"
    result = a + b
    return result

class MathOperations:
    def multiply(self, x, y):
        # internal logic
        return x * y
"""
    expected_pruned_code = """def sum_numbers(a: int, b: int) -> int:
    \"\"\"Returns the sum of two numbers.\"\"\"
    ...

class MathOperations:

    def multiply(self, x, y):
        ..."""
    
    pruned = prune_source_code(original_code)
    
    assert pruned.strip() == expected_pruned_code.strip()

def test_prune_source_code_syntax_error():
    bad_code = "def invalid_syntax(a, b) return a+b"
    with pytest.raises(SyntaxError):
        prune_source_code(bad_code)

def test_calculate_token_reduction():
    long_text = "This is a very long text " * 100
    short_text = "This is short"
    
    reduction = calculate_token_reduction(long_text, short_text)
    assert 90.0 < reduction < 99.9

    zero_reduction = calculate_token_reduction("", "")
    assert zero_reduction == 0.0

    negative_reduction = calculate_token_reduction("short", "very long text " * 10)
    assert negative_reduction < 0.0