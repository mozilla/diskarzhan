import re
import unittest
from diskarzhan.diskarzhan import lint_headers, lint_std_headers, lint_cstd_headers


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

    def test_unused_cxxcompat_header_before_c_header(self):
        code = "#include <cstdio>\n#include <stdio.h>"
        changes = lint_cstd_headers("<>", code)
        self.assertEqual(changes,
            [(1,
              '<> includes <cstdio> but does not reference any of its API')])

    def test_unused_c_header_before_cxxcompat_header(self):
        code = "#include <stdio.h>\n#include <cstdio>"
        changes = lint_cstd_headers("<>", code)
        self.assertEqual(changes,
            [(1,
              '<> includes <stdio.h> but does not reference any of its API')])

    def test_c_header_named_after_its_api(self):
        code = "#include <ctime>"
        changes = lint_cstd_headers("<>", code)
        self.assertFalse(changes)


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

    def test_unqualified_name_without_namespace_std(self):
        code = "#include <iostream>\nint main() { cout << \"hello\"; }"
        changes = lint_std_headers("<>", code)
        self.assertEqual(changes,
            [(1,
              '<> includes <iostream> but does not reference any of its API')])

    def test_unqualified_name_with_using_namespace_std(self):
        code = ("#include <iostream>\nusing namespace std;\n"
                "int main() { cout << \"hello\"; }")
        changes = lint_std_headers("<>", code)
        self.assertFalse(changes)


class LintHeadersTestCase(unittest.TestCase):
    include_re = re.compile(r'#\s*include\s*"([^"\n]+)"')
    api = {"Time.h": {"Duration"}}
    literals = {"Time.h": ("ms",)}

    def lint(self, code):
        return lint_headers("<>", code, self.api, include_re=self.include_re,
                            literals=self.literals)

    def test_unused_header(self):
        code = '\n#include "Time.h"'
        self.assertEqual(self.lint(code),
            [(2,
              '<> includes Time.h but does not reference any of its API')])

    def test_used_header(self):
        code = '#include "Time.h"\nDuration d;'
        self.assertEqual(self.lint(code), [])

    def test_unlisted_header(self):
        code = '#include "Other.h"'
        self.assertEqual(self.lint(code), [])

    def test_symbol_in_include_only(self):
        api = {"Duration.h": {"Duration"}}
        code = '#include "Duration.h"'
        changes = lint_headers("<>", code, api, include_re=self.include_re)
        self.assertEqual(changes,
            [(1,
              '<> includes Duration.h but does not reference any of its API')])

    def test_used_literal(self):
        code = '#include "Time.h"\nauto d = 10ms;'
        self.assertEqual(self.lint(code), [])

    def test_literal_suffix_in_identifier(self):
        code = '#include "Time.h"\nint items;'
        self.assertEqual(self.lint(code),
            [(1,
              '<> includes Time.h but does not reference any of its API')])

