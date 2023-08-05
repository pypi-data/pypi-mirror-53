import re

UNDERLINES_RE = re.compile("_+")
FIRST_CAP_RE = re.compile(r"(.)([A-Z][a-z]+)")
ALL_CAP_RE = re.compile("([a-z0-9])([A-Z])")


def camel_to_snake(text):
    text = FIRST_CAP_RE.sub(r"\1_\2", text)
    return ALL_CAP_RE.sub(r"\1_\2", text).lower()


def snake_to_words(text):
    return UNDERLINES_RE.sub(" ", text).strip()
