import unittest
from diskarzhan.diskarzhan import lint_std_headers, lint_cstd_headers


class UnusedCHeaderTestCase(unittest.TestCase):

    def test_trivially_unused_c_header(self):
        code = "#include <stdio.h>"
        changes = lint_cstd_headers("<>", code)
        self.assertEqual(changes,
            [(1,
              '<> includes <stdio.h> but does not reference any of its API')])

    def test_trivially_used_c_header(self):
        code = "#include <stdio.h>\nint main() { puts(\"hello\"); }"
        changes = lint_cstd_headers("<>", code)
        self.assertFalse(changes)

    def test_trivially_unused_cxxcompat_header(self):
        code = "#include <cstdio>"
        changes = lint_cstd_headers("<>", code)
        self.assertEqual(changes,
            [(1,
              '<> includes <cstdio> but does not reference any of its API')])

    def test_trivially_unused_c_header_lineno(self):
        code = "\n#include <stdio.h>"
        changes = lint_cstd_headers("<>", code)
        self.assertEqual(changes,
            [(2,
              '<> includes <stdio.h> but does not reference any of its API')])

    def test_trivially_unused_c_header_multiple_include(self):
        code = "#include <stdio.h>\n#include <stdio.h>"
        changes = lint_cstd_headers("<>", code)
        # reported only once, that's fine
        self.assertEqual(changes,
            [(1,
              '<> includes <stdio.h> but does not reference any of its API')])

    def test_trivially_unused_c_header_uncommon_include_pattern(self):
        code = "  #   include<stdio.h>"
        changes = lint_cstd_headers("<>", code)
        # reported only once, that's fine
        self.assertEqual(changes,
            [(1,
              '<> includes <stdio.h> but does not reference any of its API')])


class UnusedCXXHeaderTestCase(unittest.TestCase):
    def test_trivially_unused_cxx_header(self):
        code = "#include <iostream>"
        changes = lint_std_headers("<>", code)
        self.assertEqual(changes,
            [(1,
              '<> includes <iostream> but does not reference any of its API')])

    def test_trivially_used_cxx_header(self):
        code = "#include <iostream>\nint main() { std::cout << \"hello\"; }"
        changes = lint_std_headers("<>", code)
        self.assertFalse(changes)

    def test_trivially_unused_cxx_header_lineno(self):
        code = "\n#include <iostream>"
        changes = lint_std_headers("<>", code)
        self.assertEqual(changes,
            [(2,
              '<> includes <iostream> but does not reference any of its API')])

    def test_trivially_unused_c_header_multiple_include(self):
        code = "#include <iostream>\n#include <iostream>"
        changes = lint_std_headers("<>", code)
        # reported only once, that's fine
        self.assertEqual(changes,
            [(1,
              '<> includes <iostream> but does not reference any of its API')])

    def test_trivially_unused_c_header_uncommon_include_pattern(self):
        code = "  #   include<iostream>"
        changes = lint_std_headers("<>", code)
        # reported only once, that's fine
        self.assertEqual(changes,
            [(1,
              '<> includes <iostream> but does not reference any of its API')])

