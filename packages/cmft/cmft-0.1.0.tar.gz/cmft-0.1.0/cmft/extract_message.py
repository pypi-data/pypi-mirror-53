import re

KNOWN_FILES = {}


def extract_messages_from_diff(diff):
    files_diffs = _split_diff_into_separate_file_diffs(diff)
    for file_diff in files_diffs:
        for message in _extract_messages_from_file_diff(file_diff):
            yield message


def _split_diff_into_separate_file_diffs(diff):
    chunks = ("\n" + diff).split("\ndiff ")
    return chunks[1:]


def _extract_messages_from_file_diff(diff):
    extract = _get_extract_method_for_file_diff(diff)
    return extract(diff)


LANG_EXT = re.compile(r"^\+\+\+ .*\.(?P<ext>.*)$", re.MULTILINE)


def _get_extract_method_for_file_diff(diff):
    match = LANG_EXT.search(diff)
    ext = match.group("ext") if match else None
    return KNOWN_FILES.get(ext, _null_function)


def _null_function(diff):
    return []
