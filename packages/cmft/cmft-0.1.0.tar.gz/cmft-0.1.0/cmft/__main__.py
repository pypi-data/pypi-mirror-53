import sys

from cmft.extract_message import extract_messages_from_diff


def main():
    if len(sys.argv) > 1:
        sys.stdout.write("Usage: cmft < file.diff\n")
        sys.exit(1)
    diff = sys.stdin.read()
    messages = extract_messages_from_diff(diff)
    sys.stdout.write("\n".join(messages))


if __name__ == "__main__":
    main()
