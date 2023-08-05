import re

from cmft.utils import camel_to_snake, snake_to_words

PYTHON_TEST_RE = re.compile(r"^\+\s*def test(.*)\(", re.MULTILINE)


def extract_messages_from_python_file_diff(diff):
    matches = PYTHON_TEST_RE.findall(diff)
    return (snake_to_words(camel_to_snake(match)) for match in matches)
