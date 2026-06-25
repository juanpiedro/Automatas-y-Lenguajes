"""Test evaluation of automatas."""
import unittest
from abc import ABC

from automaton import FiniteAutomaton
from utils import AutomataFormat, deterministic_automata_isomorphism

class TestTransform(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""
    
    _test_counter = 0  # Variable estática para contar las pruebas

    def _check_transform(self, automaton, expected):
        """Test that the transformed automaton is as the expected one."""
        
        TestTransform._test_counter += 1
        test_id = TestTransform._test_counter

        automaton.draw(filename=f"deterministic_original_{test_id}", view=False)

        transformed = automaton.to_deterministic()

        transformed.draw(filename=f"deterministic_transformed_{test_id}", view=False)
        expected.draw(filename=f"deterministic_expected_{test_id}", view=False)

        equiv_map = deterministic_automata_isomorphism(expected, transformed)

        self.assertTrue(equiv_map is not None)

    def test_case1(self):
        """Test Case 1."""
        automaton_str = """
        Automaton:
        Symbols: 01
        
        q0
        qf final
        
        ini q0 -0-> qf
        qf -1-> qf
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        Symbols: 01
        
        q0
        qf final
        empty
        
        ini q0 -0-> qf
        q0 -1-> empty
        qf -0-> empty
        qf -1-> qf
        empty -0-> empty
        empty -1-> empty
        
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case2(self):
        """Test Case 2: Multiple non-deterministic transitions."""
        automaton_str = """
        Automaton:
        Symbols: ab
        
        q0
        q1
        q2 final
        
        ini q0 -a-> q1
        q0 -a-> q2
        q1 -b-> q2
        q2 -b-> q2
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        Symbols: ab
        
        q0q1q2
        q1q3 final
        q3 final
        empty
        
        ini q0q1q2 -a-> q1q3
        q0q1q2 -b-> empty
        q1q3 -a-> empty
        q1q3 -b-> q3
        q3 -a-> empty
        q3 -b-> q3
        empty -a-> empty
        empty -b-> empty
        
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case3(self):
        """Test Case 3: Lambda transitions."""
        automaton_str = """
        Automaton:
        Symbols: xy
        
        q0
        q1
        q2 final
        
        ini q0 --> q1
        q1 -x-> q2
        q0 -y-> q2
        q2 -y-> q2
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        Symbols: xy
        
        q0q1
        q2 final
        empty
        
        ini q0q1 -x-> q2
        q0q1 -y-> q2
        q2 -x-> empty
        q2 -y-> q2
        empty -x-> empty
        empty -y-> empty
        
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case4(self):
        """Test Case 4: Complex branching."""
        automaton_str = """
        Automaton:
        Symbols: 01
        
        q0
        q1
        q2
        q3 final
        
        ini q0 -0-> q1
        q0 -1-> q2
        q1 -0-> q3
        q1 -1-> q1
        q2 -0-> q2
        q2 -1-> q3
        q3 -0-> q3
        q3 -1-> q3
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        Symbols: 01
        
        q0
        q1
        q2
        q3 final
        
        ini q0 -0-> q1
        q0 -1-> q2
        q1 -0-> q3
        q1 -1-> q1
        q2 -0-> q2
        q2 -1-> q3
        q3 -0-> q3
        q3 -1-> q3
        
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case5(self):
        """Test Case 5: Multiple final states with non-determinism."""
        automaton_str = """
        Automaton:
        Symbols: ab
        
        q0
        q1 final
        q2 final
        q3
        
        ini q0 -a-> q1
        q0 -a-> q3
        q1 -b-> q2
        q3 -b-> q2
        q3 -a-> q1
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        Symbols: ab
        
        q0
        q1q3 final
        q1 final
        q2 final
        empty
        
        ini q0 -a-> q1q3
        q0 -b-> empty
        q1q3 -a-> q1
        q1q3 -b-> q2
        q1 -a-> empty
        q1 -b-> q2
        q2 -a-> empty
        q2 -b-> empty
        empty -a-> empty
        empty -b-> empty
        
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case6(self):
        """Test Case 6: Self-loops and cycles."""
        automaton_str = """
        Automaton:
        Symbols: 01
        
        q0
        q1 final
        
        ini q0 -0-> q0
        q0 -1-> q1
        q0 -1-> q0
        q1 -0-> q1
        q1 -1-> q0
        """

        automaton = AutomataFormat.read(automaton_str)

        expected_str = """
        Automaton:
        Symbols: 01
        
        q0
        q0q1 final
        
        ini q0 -0-> q0
        q0 -1-> q0q1
        q0q1 -0-> q0q1
        q0q1 -1-> q0q1
        
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)


if __name__ == '__main__':
    unittest.main()
