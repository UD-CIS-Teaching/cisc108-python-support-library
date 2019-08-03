import re


def generate_regex(successOrFailure: bool, message: str) -> str:
    regex: str = r"SUCCESS - \[line \d+\] " if successOrFailure else r"FAILURE - \[line \d+\] "
    regex += re.escape(message)
    return regex
