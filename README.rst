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
    assert_equal(add5(10), 5.0)

