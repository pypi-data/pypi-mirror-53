import re
import sys


'''
Format of input string will be changed according to pytest requirements.
The 'directory' variable defines the root directory of the repository.
Examples:
    input: 'repo.core.tests.test_account.TestCase'
    output: ['django-sites/repo/core/tests/test_account.py::TestCase']
'''

directory = "django-sites"


def handling_references(user_references):
    """ handles multiple or one reference and returns a list of strings to match the manage.py requirements """
    result = ''
    for reference in user_references:
        adjusted_reference = rearrange_string(reference)
        result += ' ' + adjusted_reference
    return result.strip().split()


def rearrange_string(user_input):
    """ rearranging string according to pytest standard format """
    user_input = complete_string(user_input)
    user_input = unify_input(user_input)
    user_input_as_list = user_input.split('.')
    user_input_as_list = format_string_for_pytest(user_input_as_list)
    return "".join(user_input_as_list)


def complete_string(user_input):
    """ adds the directory name with a leading slash and .py to the string """
    user_input = user_input.replace('.py', '', 1)
    user_input.lstrip("/")
    if directory not in user_input:
        user_input = directory + '/' + user_input
    return user_input


def unify_input(user_input):
    """ changes all separators (except underscore and dash) to dots """
    pattern = re.compile(r'[^A-Za-z0-9_\-\.]+')
    if re.search(pattern, user_input):
        return pattern.sub(".", user_input)
    return user_input


def format_string_for_pytest(user_input_as_list):
    """ rebuilds the user input as needed for pytest """
    before_module = True
    for counter, element in enumerate(user_input_as_list):
        if 'test_' in element and before_module:
            user_input_as_list[counter] += ".py"
            before_module = False
        if len(user_input_as_list) is not counter + 1:  # counter starts with 0 so +1 is needed
            user_input_as_list[counter] = extend_string(user_input_as_list[counter], before_module)
    return user_input_as_list


def extend_string(extend_element, before_module):
    """ translates the separating dots to slashes before filename or to quad points after the filename  """
    if before_module:
        extend_element += "/"
    else:
        extend_element += "::"
    return extend_element


if __name__ == '__main__':
    print handling_references(sys.argv[1:])
