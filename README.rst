CISC108 Support Library
=======================

A collection of tools to help students write code.

For now, mostly improved assertions.

Installation
============

Install from PyPi::
    
    pip install cisc108

Or install from the https://github.com/UD-CIS-Teaching/cisc108-python-support-library

Examples
========

.. code-block:: python
    
    from cisc108 import assert_equal
    
    def halve(number):
        return number / 2
    
    # Correctly handles floating points
    assert_equal(halve(10), 5.0)
    
.. code-block:: python

    from cisc108 import assert_type
    
    def make_list(num1, num2):
        return [num1, num2]
    
    assert_type(make_list(5, 7), list)


.. code-block:: python

    # What if we failed a test?
    assert_type(make_list(5, 7), int)
    # FAILURE - [line 5], value was the wrong type. Expected type was 'integer', but actual value was [5, 7] ('list').
    
Output
======

This library will print a message to STDOUT if an assertion fails, and returns True/False. It does not raise an exception or print to STDERR.

Supported Types
===============

* Numbers: strictly compares numeric types, but allows floats to have imprecision, defaults to 4 places
* Strings: can strictly compare types with exact_strings=True, but defaults to ignore whitespace on newlines and capitalization
* Lists, Tuples: applies same rules to inner types as container types
* Sets, Frozensets, Dictionary: checks that all elements are contained in both, in any order
* Generators: functions like `enumerate` and `.items()` that produce generators are converted to lists and sets (as appropriate), then checked that their values match.
* Other types should work as well, but require that the result of `type` match, and that `x == y`
