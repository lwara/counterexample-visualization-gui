import re

def is_valid_uclid_code(code):
    # Syntax checking
    valid_syntax = check_syntax(code)
    if not valid_syntax:
        return False, "Syntax error"

    # Semantic analysis
    valid_semantics = check_semantics(code)
    if not valid_semantics:
        return False, "Semantic error"

    return True, "Code is valid Uclid 5"

def check_syntax(code):
    # Check module declaration
    valid_module = re.match(r'^module\s+\w+\s*{.*}', code, re.MULTILINE | re.DOTALL) is not None

    # Check init block
    valid_init = re.match(r'^\s*init\s*{.*}', code, re.MULTILINE | re.DOTALL) is not None

    # Check next block
    valid_next = re.match(r'^\s*next\s*{.*}', code, re.MULTILINE | re.DOTALL) is not None

    # Check control block
    valid_control = re.match(r'^\s*control\s*{.*}', code, re.MULTILINE | re.DOTALL) is not None

    return valid_module and valid_init and valid_next and valid_control

def check_semantics(code):
    # Perform semantic analysis
    # For simplicity, assume all code is semantically valid
    return True

# Example usage
code = """
module example {
    var x: int;
    init {
        x = 0;
    }
    next {
        x' = x + 1;
    }
    control {
        assert(x <= 10);
    }
}
"""

valid, message = is_valid_uclid_code(code)
print(message)
