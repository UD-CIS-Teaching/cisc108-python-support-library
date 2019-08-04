import re
import sys
import os
from contextlib import contextmanager
from io import StringIO

cisc108_library = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, cisc108_library)


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def generate_regex(successOrFailure: bool, message: str) -> str:
    regex: str = r"SUCCESS - \[line \d+\] " if successOrFailure else r"FAILURE - \[line \d+\] "
    regex += re.escape(message)
    return regex
