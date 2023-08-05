from cmft.extract_from_python import extract_messages_from_python_file_diff
from cmft.extract_message import KNOWN_FILES

KNOWN_FILES["py"] = extract_messages_from_python_file_diff
