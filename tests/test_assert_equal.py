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

        with captured_output() as (out, err):
            self.assertFalse(assert_equal([1, 2, 3.0], [1, 2, 3]))
        self.assertEqual(out.getvalue().strip(),
                         "FAILURE - [line 80] self.assertFalse(assert_equal([1, 2, 3.0], [1, 2, 3])), predicted answer was [1, 2, 3], computed answer was [1, 2, 3.0].")
                         
    def test_sets(self):
        with captured_output() as (out, err):
            self.assertTrue(assert_equal({1, 5, 5, 'Test'}, {1, 5, 'test', 'test'}))
        self.assertEqual(out.getvalue().strip(),
                         "SUCCESS - [line 86] self.assertTrue(assert_equal({1, 5, 5, 'Test'}, {1, 5, 'test', 'test'}))")
    
        with captured_output() as (out, err):
            self.assertFalse(assert_equal({1, 2}, {1, 2, 3}))
        self.assertEqual(out.getvalue().strip(),
                         "FAILURE - [line 91] self.assertFalse(assert_equal({1, 2}, {1, 2, 3})), predicted answer was {1, 2, 3}, computed answer was {1, 2}.")

        with captured_output() as (out, err):
            self.assertFalse(assert_equal({1, 2, 3}, {1, 2, 4}))
        self.assertEqual(out.getvalue().strip(),
                         "FAILURE - [line 96] self.assertFalse(assert_equal({1, 2, 3}, {1, 2, 4})), predicted answer was {1, 2, 4}, computed answer was {1, 2, 3}.")
    
    def test_dicts(self):
        with captured_output() as (out, err):
            self.assertTrue(assert_equal({1.0: 5, 'Test': True}, {'Test': True, 1.0: 5}))
        self.assertEqual(out.getvalue().strip(),
                         "SUCCESS - [line 102] self.assertTrue(assert_equal({1.0: 5, 'Test': True}, {'Test': True, 1.0: 5}))")
    
        with captured_output() as (out, err):
            self.assertFalse(assert_equal({1: 2}, {1: 2, 3: 5}))
        self.assertEqual(out.getvalue().strip(),
                         "FAILURE - [line 107] self.assertFalse(assert_equal({1: 2}, {1: 2, 3: 5})), predicted answer was {1: 2, 3: 5}, computed answer was {1: 2}.")

        with captured_output() as (out, err):
            self.assertFalse(assert_equal({1.0: 5}, {1: 5}))
        self.maxDiff = None
        self.assertEqual(out.getvalue().strip(),
                         "FAILURE - [line 112] self.assertFalse(assert_equal({1.0: 5}, {1: 5})), predicted answer was {1: 5}, computed answer was {1.0: 5}.")

        with captured_output() as (out, err):
            self.assertFalse(assert_equal({'Test': False}, {'Test': True}))
        self.maxDiff = None
        self.assertEqual(out.getvalue().strip(),
                         "FAILURE - [line 118] self.assertFalse(assert_equal({'Test': False}, {'Test': True})), predicted answer was {'Test': True}, computed answer was {'Test': False}.")
 
    def test_generators(self):
        with captured_output() as (out, err):
            self.assertTrue(assert_equal(range(5), [0, 1, 2, 3, 4]))
        self.assertEqual(out.getvalue().strip(),
                         "SUCCESS - [line 125] self.assertTrue(assert_equal(range(5), [0, 1, 2, 3, 4]))")
        
        with captured_output() as (out, err):
            self.assertTrue(assert_equal([0, 1, 2, 3, 4], range(5)))
        self.assertEqual(out.getvalue().strip(),
                         "SUCCESS - [line 130] self.assertTrue(assert_equal([0, 1, 2, 3, 4], range(5)))")

        with captured_output() as (out, err):
            self.assertFalse(assert_equal(5, range(5)))
        self.assertEqual(out.getvalue().strip(),
                         "FAILURE - [line 135] self.assertFalse(assert_equal(5, range(5))), predicted answer was range(0, 5) ('range'), computed answer was 5 ('int'). You attempted to compare unrelated data types.")
                         
        with captured_output() as (out, err):
            self.assertFalse(assert_equal({1: 2, 4: 3}.items(), [(1, 2), (3, 4)]))
        self.assertEqual(out.getvalue().strip(),
                         "FAILURE - [line 140] self.assertFalse(assert_equal({1: 2, 4: 3}.items(), [(1, 2), (3, 4)])), predicted answer was [(1, 2), (3, 4)], computed answer was dict_items([(1, 2), (4, 3)]).")
                         
        with captured_output() as (out, err):
            self.assertTrue(assert_equal({1: 2, 3: 4}.items(), [(1, 2), (3, 4)]))
        self.assertEqual(out.getvalue().strip(),
                         "SUCCESS - [line 145] self.assertTrue(assert_equal({1: 2, 3: 4}.items(), [(1, 2), (3, 4)]))")
    
    def test_classes(self):
        self.maxDiff = None
        
        class Dog:
            def __init__(self, name, breed):
                self.name = name
                self.breed = breed
            
            def __repr__(self):
                return self.name
        
        ada = Dog('ada', 'corgi')
        evil_ada = Dog('ada', 'corgi')
        my_dog = ada
        klaus = Dog('klaus', 'schnauzer')
        
        with captured_output() as (out, err):
            self.assertTrue(assert_equal(ada, my_dog))
        self.assertEqual(out.getvalue().strip(),
                         "SUCCESS - [line 166] self.assertTrue(assert_equal(ada, my_dog))")
        
        with captured_output() as (out, err):
            self.assertFalse(assert_equal(5, my_dog))
        self.assertEqual(out.getvalue().strip(),
                         "FAILURE - [line 171] self.assertFalse(assert_equal(5, my_dog)), predicted answer was ada ('Dog'), computed answer was 5 ('int'). You attempted to compare unrelated data types.")
                         
        with captured_output() as (out, err):
            self.assertFalse(assert_equal(ada, evil_ada))
        self.assertEqual(out.getvalue().strip(),
                         "FAILURE - [line 176] self.assertFalse(assert_equal(ada, evil_ada)), predicted answer was ada, computed answer was ada.")
        
        with captured_output() as (out, err):
            self.assertFalse(assert_equal(ada, klaus))
        self.assertEqual(out.getvalue().strip(),
                         "FAILURE - [line 181] self.assertFalse(assert_equal(ada, klaus)), predicted answer was klaus, computed answer was ada.")
                         
    
                         
    def test_frozensets(self):
        a = frozenset((1, 5, 5, 'Test'))
        b = frozenset((1, 5, 'Test', 'Test'))
        with captured_output() as (out, err):
            self.assertTrue(assert_equal(a, b))
        self.assertEqual(out.getvalue().strip(),
                         "SUCCESS - [line 191] self.assertTrue(assert_equal(a, b))")
    
        c = frozenset((1, 2))
        d = frozenset((1, 2, 3))
        with captured_output() as (out, err):
            self.assertFalse(assert_equal(c, d))
        self.assertEqual(out.getvalue().strip(),
                         "FAILURE - [line 198] self.assertFalse(assert_equal(c, d)), predicted answer was frozenset({1, 2, 3}), computed answer was frozenset({1, 2}).")
                         
    def test_traceback_shim(self):
        # Mock out traceback
        import importlib
        old = sys.modules.copy()
        sys.modules['traceback'] = None
        import cisc108
        
        with captured_output() as (out, err):
            self.assertTrue(cisc108.assert_equal(5, 5))
        self.assertEqual(out.getvalue().strip(), "SUCCESS")
        
        with captured_output() as (out, err):
            self.assertFalse(cisc108.assert_equal(5, 5.0))
        self.assertEqual(out.getvalue().strip(), "FAILURE, predicted answer was 5.0 ('float'), computed answer was 5 ('int'). You attempted to compare unrelated data types.")
        
        # Restore traceback
        sys.modules['traceback'] = old['traceback']

if __name__ == '__main__':
    unittest.main(buffer=False)
