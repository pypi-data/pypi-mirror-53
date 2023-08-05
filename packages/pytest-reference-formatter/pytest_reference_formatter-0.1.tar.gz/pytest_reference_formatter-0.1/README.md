# Formatter

TL;DR: Input string will be changed to match pytest requirements.
- **Input:** Strings separated by spaces
- **Return:** List of strings

## Details
- The [formatter](pytest_reference_formatter/formatter.py) changes a string (e.g. copied from the "Copy Reference" function from PyCharm) to match the pytest requirements.
- The script can handle multiple input strings seperated by a space and returns a modified list of strings. 


## Example of Usage
**Input:**

    python formatter.py "repo.core.tests.test_account.TestCase repo2.core2.tests2.test_account2.TestCase2.test_function"
**Output:**

    ['django-sites/repo/core/tests/test_account.py::TestCase', 'django-sites/repo2/core2/tests2/test_account2.py::TestCase2::test_function']
    
The root directory *django-sites* seen at *output* is a variable that can be changed inside the [formatter](pytest_reference_formatter/formatter.py).

