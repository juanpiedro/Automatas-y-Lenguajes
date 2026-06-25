#!/usr/bin/env python

import re
import unittest

from regular_expressions import RE0, RE1, RE2, RE3, RE4, RE5, RE6


class TestP0(unittest.TestCase):
    """Tests of assignment 0."""

    def check_expression(self, expr: str, string: str, expected: bool) -> None:
        with self.subTest(string=string):
            match = re.fullmatch(expr, string)
            self.assertEqual(bool(match), expected)

    def test_exercise_0(self) -> None:
        self.check_expression(RE0, "a", True)
        self.check_expression(RE0, "bbbbaba", True)
        self.check_expression(RE0, "abbab", False)
        self.check_expression(RE0, "b", False)
        # Additional tests
        self.check_expression(RE0, "aa", True)
        self.check_expression(RE0, "ba", True)
        self.check_expression(RE0, "bb", False)
        self.check_expression(RE0, "abab", False)
        self.check_expression(RE0, "", False)

    def test_exercise_1(self) -> None:
        self.check_expression(RE1, "", True)
        self.check_expression(RE1, "00", True)
        self.check_expression(RE1, "110101", True)
        self.check_expression(RE1, "1", False)
        self.check_expression(RE1, "1ba", False)
        # Additional tests
        self.check_expression(RE1, "111", False)
        self.check_expression(RE1, "11", True)
        self.check_expression(RE1, "1010", True)
        self.check_expression(RE1, "1001", True)
        self.check_expression(RE1, "101111", False)
        self.check_expression(RE1, "10011", False)

    def test_exercise_2(self) -> None:
        self.check_expression(RE2, "01", True)
        self.check_expression(RE2, "10", True)
        self.check_expression(RE2, "0101", True)
        self.check_expression(RE2, "1010", True)
        self.check_expression(RE2, "001", False)
        self.check_expression(RE2, "110", False)
        self.check_expression(RE2, "000", False)
        self.check_expression(RE2, "111", False)

    def test_exercise_3(self) -> None:
        self.check_expression(RE3, "0", True)
        self.check_expression(RE3, "12", True)
        self.check_expression(RE3, "-1321", True)
        self.check_expression(RE3, "00", False)
        self.check_expression(RE3, "+3.14", True)
        self.check_expression(RE3, "42.0", True)
        self.check_expression(RE3, "012", False)
        self.check_expression(RE3, "3.", False)
        self.check_expression(RE3, "-0.5", True)
        self.check_expression(RE3, "+0", True)
        self.check_expression(RE3, "01", False)
        self.check_expression(RE3, "-.5", False)

    def test_exercise_4(self) -> None:
        self.check_expression(RE4, "nombre.apellido@estudiante.uam.es", True)
        self.check_expression(RE4, "nombre.apellido@uam.es", True)
        self.check_expression(RE4, "nombre.apellido@uam.com", False)
        self.check_expression(RE4, "nombre.apellidouam.com", False)
        self.check_expression(RE4, "nombreapellido@uam.com", False)
        self.check_expression(RE4, "juan.perez@estudiante.uam.es", True)
        self.check_expression(RE4, "ana.garcia@uam.es", True)
        self.check_expression(RE4, "nombre.apellido@uam.org", False)
        self.check_expression(RE4, "nombreapellido@estudiante.uam.es", False)

    def test_exercise_5(self) -> None:
        self.check_expression(RE5, "23/04/2025", True)
        self.check_expression(RE5, "00/01/2020", False)
        self.check_expression(RE5, "15/00/2020", False)
        self.check_expression(RE5, "01/01/2000", True)
        self.check_expression(RE5, "31/12/1999", True)
        self.check_expression(RE5, "32/01/2020", False)
        self.check_expression(RE5, "15/13/2020", False)

    def test_exercise_6(self) -> None:
        self.check_expression(RE6, "132.0.21.4", True)
        self.check_expression(RE6, "192.168.1.1", True)
        self.check_expression(RE6, "256.1.1.1", False)
        self.check_expression(RE6, "0.0.0.0", True)
        self.check_expression(RE6, "255.255.255.255", True)
        self.check_expression(RE6, "192.168.1.256", False)
        self.check_expression(RE6, "01.02.03.04", False)

if __name__ == '__main__':
    unittest.main()
