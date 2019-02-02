import unittest
import os
import sys
from textwrap import dedent
from io import StringIO
from contextlib import contextmanager

cisc108_library = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, cisc108_library)

from cisc108 import assert_equal

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

class TestAssertEqual(unittest.TestCase):

    def test_integers(self):
        with captured_output() as (out, err):
            self.assertTrue(assert_equal(5, 5))
        self.assertEqual(out.getvalue().strip(),
                         "SUCCESS - [line 27] self.assertTrue(assert_equal(5, 5))")
    
        with captured_output() as (out, err):
            self.assertFalse(assert_equal(5, 10))
        self.assertEqual(out.getvalue().strip(),
                         "FAILURE - [line 32] self.assertFalse(assert_equal(5, 10)), predicted answer was 10, computed answer was 5.")
                         
        with captured_output() as (out, err):
            self.assertFalse(assert_equal(5, 10.0))
        self.assertEqual(out.getvalue().strip(),
                         "FAILURE - [line 37] self.assertFalse(assert_equal(5, 10.0)), predicted answer was 10.0 ('float'), computed answer was 5 ('int'). You attempted to compare unrelated data types.")
     
    def test_floats(self):
        with captured_output() as (out, err):
            self.assertTrue(assert_equal(10/2, 5.0))
        self.assertEqual(out.getvalue().strip(),
                         "SUCCESS - [line 43] self.assertTrue(assert_equal(10/2, 5.0))")
    
        with captured_output() as (out, err):
            self.assertFalse(assert_equal(3.1, 3.2))
        self.assertEqual(out.getvalue().strip(),
                         "FAILURE - [line 48] self.assertFalse(assert_equal(3.1, 3.2)), predicted answer was 3.2, computed answer was 3.1.")
     
    def test_strings(self):
        with captured_output() as (out, err):
            self.assertTrue(assert_equal('Hello world!', 'Hello world!'))
        self.assertEqual(out.getvalue().strip(),
                         "SUCCESS - [line 54] self.assertTrue(assert_equal('Hello world!', 'Hello world!'))")
                         
        with captured_output() as (out, err):
            self.assertTrue(assert_equal('Hello world!', 'Hello World!'))
        self.assertEqual(out.getvalue().strip(),
                         "SUCCESS - [line 59] self.assertTrue(assert_equal('Hello world!', 'Hello World!'))")
    
        with captured_output() as (out, err):
            self.assertFalse(assert_equal('Hello world!', 'Hello World!', exact_strings=True))
        self.assertEqual(out.getvalue().strip(),
                         "FAILURE - [line 64] self.assertFalse(assert_equal('Hello world!', 'Hello World!', exact_strings=True)), predicted answer was 'Hello World!', computed answer was 'Hello world!'.")
                         
    def test_sequences(self):
        with captured_output() as (out, err):
            self.assertTrue(assert_equal([1, 5.0, 'Test'], [1, 5.0, 'test']))
        self.assertEqual(out.getvalue().strip(),
                         "SUCCESS - [line 70] self.assertTrue(assert_equal([1, 5.0, 'Test'], [1, 5.0, 'test']))")
    
        with captured_output() as (out, err):
            self.assertFalse(assert_equal([1, 2], [1, 2, 3]))
        self.assertEqual(out.getvalue().strip(),
                         "FAILURE - [line 75] self.assertFalse(assert_equal([1, 2], [1, 2, 3])), predicted answer was [1, 2, 3], computed answer was [1, 2].")

if __name__ == '__main__':
    unittest.main(buffer=False)
