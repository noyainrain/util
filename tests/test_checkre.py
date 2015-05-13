# checkre
# https://github.com/NoyaInRain/util/blob/master/checkre.py
# by Sven James <sven.jms AT gmail.com>
# released into the public domain

# Python forward compatibility
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from io import StringIO
from unittest import TestCase
from checkre import (
    checkre, line_length_check, simple_indentation_check, trailing_space_check,
    header_check, whitespace_check, newline_at_eof_check)

class ModuleTest(TestCase):
    def test_checkre(self):
        config = {r'checkre-test\.txt': (
            line_length_check(),
            simple_indentation_check(),
            trailing_space_check(),
            header_check(StringIO('tests:\n'), 1),
            whitespace_check(),
            newline_at_eof_check()
        )}
        self.assertEqual(checkre(config, 'tests/res'), 1)
