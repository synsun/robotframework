import unittest

from robot.utils.asserts import *

from robot.running.runkwregister import _RunKeywordRegister as Register
from robot.utils import PY2, PY3


class Lib:
    
    def method_without_arg(self):
        pass
    
    def method_with_one(self, name, *args):
        pass
    
    def method_with_default(self, one, two, three='default', *args):
        pass


def function_without_arg():
    pass

def function_with_one(name, *args):
    pass

def function_with_three(one, two, three, *args):
    pass


class TestRunKeywordRegister(unittest.TestCase):

    def setUp(self):
        self.reg = Register()
    
    def test_register_run_keyword_method_with_kw_name_and_arg_count(self):
        self._verify_reg('My Lib', 'myKeyword', 'My Keyword', 3, 3)

    if PY2:
        def test_register_run_keyword_method_with_kw_name_without_arg_count(self):
            assert_raises(ValueError, self.reg.register_run_keyword, 'My Lib', 'my_keyword')
        
    def test_register_run_keyword_method_with_function_without_arg(self):
        self._verify_reg('My Lib', function_without_arg, 'Function Without Arg', 0)
    
    def test_register_run_keyword_method_with_function_with_one_arg(self):
        self._verify_reg('My Lib', function_with_one, 'Function With One', 1)

    def test_register_run_keyword_method_with_function_with_three_arg(self):
        self._verify_reg('My Lib', function_with_three, 'Function With Three', 3)

    def test_register_run_keyword_method_with_method_without_arg(self):
        self._verify_reg('My Lib', Lib().method_without_arg, 'Method Without Arg', 0)

    def test_register_run_keyword_method_with_method_with_one_arg(self):
        self._verify_reg('My Lib', Lib().method_with_one, 'Method With One', 1)

    def test_register_run_keyword_method_with_method_with_default_arg(self):
        self._verify_reg('My Lib', Lib().method_with_default, 'Method With Default', 3)

    if PY2:
        def test_register_run_keyword_method_with_invalid_keyword_type(self):
            assert_raises(ValueError, self.reg.register_run_keyword, 'My Lib', 1)
    
    def test_get_arg_count_with_non_existing_keyword(self):
        assert_equal(self.reg.get_args_to_process('My Lib', 'No Keyword'), -1)

    def test_get_arg_count_with_non_existing_library(self):
        self._verify_reg('My Lib', 'get_arg', 'Get Arg', 3, 3)
        assert_equal(self.reg.get_args_to_process('No Lib', 'Get Arg'), -1)

    if PY2:

        def test_is_run_keyword_when_library_does_not_match(self):
            self.reg.register_run_keyword('SomeLib', function_without_arg)
            assert_false(self.reg.is_run_keyword('Non Existing Lib', 'whatever'))

        def test_is_run_keyword_when_keyword_does_not_match(self):
            self.reg.register_run_keyword('SomeLib', function_without_arg)
            assert_false(self.reg.is_run_keyword('SomeLib', 'non_existing'))

        def test_is_run_keyword_matches(self):
            self.reg.register_run_keyword('SomeLib', function_without_arg)
            self.reg.register_run_keyword('AnotherLib', Lib().method_with_default)
            assert_true(self.reg.is_run_keyword('SomeLib', 'Function Without Arg'))
            assert_true(self.reg.is_run_keyword('AnotherLib', 'Method With Default'))

    def _verify_reg(self, lib_name, keyword, keyword_name, arg_count, given_count=None):
        if given_count is None:
            if PY3:
                return
            self.reg.register_run_keyword(lib_name, keyword)
        else:
            self.reg.register_run_keyword(lib_name, keyword, given_count)
        assert_equal(self.reg.get_args_to_process(lib_name, keyword_name), arg_count)


if __name__ == '__main__':
    unittest.main()
