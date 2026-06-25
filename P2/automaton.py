"""
    Equipo docente de Autómatas y Lenguajes Curso 2025-26
    Última modificación: 18 de septiembre de 2025
"""

from collections import deque
from graphviz import Digraph
from utils import is_deterministic
from typing import Dict
import random

"""
    Podéis implementar cualquier función auxiliar que consideréis necesaria
"""

class FiniteAutomaton:

    def __init__(self, initial_state, states, symbols, transitions, final_states):
        self.transitions = transitions
        self.states = states
        self.symbols = symbols
        self.initial_state = initial_state
        self.final_states = final_states

    def add_transition(self, start_state, symbol, end_state):
        try:
            t_state = self.transitions[start_state]
        except KeyError:
            self.transitions[start_state] = {}
            t_state = self.transitions[start_state]
        try:
            t_state[symbol].append(end_state)
        except KeyError:
            t_state[symbol] = []
            t_state[symbol].append(end_state)

    def complete_lambdas(self, estados_actuales: list):
        estados_iter = []

        for actual_state in estados_actuales:
            try:
                for lamda in self.transitions[actual_state][None]:
                    if lamda not in estados_actuales:
                        estados_actuales.append(lamda)
                        estados_iter.append(lamda)
            except:
                pass
        while len(estados_iter) != 0:
            estados_prev_iter = estados_iter
            estados_iter = []
            for actual_state in estados_prev_iter:
                try:
                    for lamda in self.transitions[actual_state][None]:
                        if lamda not in estados_actuales:
                            estados_actuales.append(lamda)
                            estados_iter.append(lamda)
                except:
                    pass
        return estados_actuales
    
    def consumir_caracter(self, actual_states, caracter):
        previous_states = actual_states
        actual_states = []
        for state in previous_states:
            try:
                for new_State in self.transitions[state][caracter]:
                    actual_states.append(new_State)
            except KeyError:
                pass
        if len(actual_states) == 0:
            return None
        return actual_states

    def accepts(self, cadena):
        actual_states = [self.initial_state]
        actual_states = self.complete_lambdas(actual_states)

        for caracter in cadena:
            actual_states = self.consumir_caracter(actual_states, caracter)
            if actual_states == None:
                return False
            actual_states = self.complete_lambdas(actual_states)

        for estado in actual_states:
            if estado in self.final_states:
                return True
        return False

    def create_new_ini_state(self, state_list, new_automaton: "FiniteAutomaton", to_process):
        if str(state_list) in new_automaton.states:
            return None
        new_automaton.states.add(str(state_list))
        for symbol in self.symbols:
            reacheable_states = []
            for state in state_list:
                reacheable_states += self.transitions[state].get(symbol, [])
            reacheable_states = self.complete_lambdas(reacheable_states)
            if not str(reacheable_states) in new_automaton.states:
                to_process.add(reacheable_states)
            new_automaton.transitions[str(state_list)][symbol] = str(reacheable_states)
        return to_process
            

    def to_deterministic(self):
        new_automaton = FiniteAutomaton("", [], set(), {}, set())
        lambdas = self.complete_lambdas([self.initial_state])
        lambdas.sort()
        to_process = [lambdas]
        while len(to_process) > 0:
            state_list = to_process.pop()
            if str(state_list) in new_automaton.states:
                continue
            new_automaton.states.append(str(state_list))
            # print(self.symbols)
            for symbol in self.symbols:
                reacheable_states = []
                for state in state_list:
                    # print(state_list, state)
                    reacheable_states += self.transitions.get(state, {}).get(symbol, [])
                reacheable_states = self.complete_lambdas(list(set(reacheable_states)))
                reacheable_states = list(set(reacheable_states))
                reacheable_states.sort()
                if len(reacheable_states) == 0:
                    continue
                if not str(reacheable_states) in new_automaton.states:
                    to_process.append(reacheable_states)
                if not str(state_list) in new_automaton.transitions.keys():
                    new_automaton.transitions[str(state_list)] = {}
                new_automaton.transitions[str(state_list)][symbol] = [str(reacheable_states)]
        new_automaton.symbols = self.symbols
        new_automaton.initial_state = str(lambdas)
        finals = []
        for state in self.final_states:
            for new_state in new_automaton.states:
                if state in new_state:
                    finals.append(new_state)
        
        new_automaton.final_states = set(finals)

        sumidero_added = False
        for state in new_automaton.states:
            for symbol in new_automaton.symbols:
                if new_automaton.transitions.get(state, {}).get(symbol, None) == None:
                    new_automaton.add_transition(state, symbol, "sumidero")
                    sumidero_added = True
        if sumidero_added:
            new_automaton.states += ["sumidero"]
            for symbol in new_automaton.symbols:
                new_automaton.add_transition("sumidero", symbol, "sumidero")

        return new_automaton

            
                
                


    def to_minimized(self):
        ret_automato = self.to_deterministic()
        # DFS desde el estado inicial para obtener los estados alcanzables
        reachable_states = []
        stack = [ret_automato.initial_state]
        visited = set()
        while stack:
            current_state = stack.pop()
            if current_state not in visited:
                visited.add(current_state)
                reachable_states.append(current_state)
                if current_state in ret_automato.transitions:
                    for symbol in ret_automato.transitions[current_state]:
                        for neighbor in ret_automato.transitions[current_state][symbol]:
                            if neighbor not in visited:
                                stack.append(neighbor)
        ret_automato.states = reachable_states
        
        # Minimización usando el algoritmo de partición
        equivalence_table = {}
        for state_aux in ret_automato.states:
            if state_aux in ret_automato.final_states:
                equivalence_table[state_aux] = 1
            else:
                equivalence_table[state_aux] = 0
        changed = True
        while changed:
            changed = False
            new_equivalence_table = {}
            for state in ret_automato.states:
                signature = [equivalence_table[state]]
                for symbol in ret_automato.symbols:
                    try:
                        dest_state = ret_automato.transitions[state][symbol][0]
                        signature.append(equivalence_table[dest_state])
                    except KeyError:
                        signature.append(None)
                signature = tuple(signature)
                new_equivalence_table[state] = signature
            # Reasignar IDs
            signature_to_id = {}
            id_counter = 0
            for state in ret_automato.states:
                signature = new_equivalence_table[state]
                if signature not in signature_to_id:
                    signature_to_id[signature] = id_counter
                    id_counter += 1
            final_equivalence_table = {}
            for state in ret_automato.states:
                signature = new_equivalence_table[state]
                final_equivalence_table[state] = signature_to_id[signature]
            if final_equivalence_table != equivalence_table:
                changed = True
            equivalence_table = final_equivalence_table
        
        # Construir el autómata minimizado
        minimized_automaton = FiniteAutomaton("", set(), ret_automato.symbols, {}, set())
        state_repr = {}
        for state in ret_automato.states:
            eq_class = equivalence_table[state]
            if eq_class not in state_repr:
                state_repr[eq_class] = f"q{eq_class}"
                minimized_automaton.states.add(f"q{eq_class}")
            if state == ret_automato.initial_state:
                minimized_automaton.initial_state = state_repr[eq_class]
            if state in ret_automato.final_states:
                minimized_automaton.final_states.add(state_repr[eq_class])
        
        # Agregar transiciones
        added_transitions = set()
        for state in ret_automato.states:
            src_repr = state_repr[equivalence_table[state]]
            for symbol in ret_automato.symbols:
                try:
                    dest_state = ret_automato.transitions[state][symbol][0]
                    dest_repr = state_repr[equivalence_table[dest_state]]
                    # Agregar transición solo si no existe ya
                    if (src_repr, symbol) not in added_transitions:
                        if src_repr not in minimized_automaton.transitions:
                            minimized_automaton.transitions[src_repr] = {}
                        minimized_automaton.transitions[src_repr][symbol] = [dest_repr]
                        added_transitions.add((src_repr, symbol))
                except KeyError:
                    pass
        
        return minimized_automaton

    def draw(self, path="./images/", filename="automata", view=False):
        dot = Digraph(comment="Automata", format="png")
        dot.attr(rankdir="LR")

        # Nodo invisible para punto inicial
        dot.node("", shape="none")

        # Almacenar estados
        for state in self.states:
            if state in self.final_states:
                dot.node(state, shape="doublecircle")
            else:
                dot.node(state, shape="circle")
        
        # Flecha al estado inicial
        dot.edge("", self.initial_state)

        # Almacenar transiciones
        for state_ini in self.transitions:
            for symbol in self.transitions[state_ini]:
                for state_fin in self.transitions[state_ini][symbol]:
                    dot.edge(state_ini, state_fin, symbol if symbol is not None else "λ")
        dot.render(path+filename, view=view)
