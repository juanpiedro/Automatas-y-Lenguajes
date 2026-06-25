from __future__ import annotations

from collections import deque
from typing import AbstractSet, Collection, MutableSet, Optional, Dict, List, Optional
import copy

class RepeatedCellError(Exception):
    """Exception for repeated cells in LL(1) tables."""

class SyntaxError(Exception):
    """Exception for parsing errors."""

class Grammar:
    """
    Class that represents a grammar.

    Args:
        terminals: Terminal symbols of the grammar.
        non_terminals: Non terminal symbols of the grammar.
        productions: Dictionary with the production rules for each non terminal
          symbol of the grammar.
        axiom: Axiom of the grammar.

    """

    def __init__(
        self,
        terminals: AbstractSet[str],
        non_terminals: AbstractSet[str],
        productions: Dict[str, List[str]],
        axiom: str,
    ) -> None:
        if terminals & non_terminals:
            raise ValueError(
                "Intersection between terminals and non terminals "
                "must be empty.",
            )

        if axiom not in non_terminals:
            raise ValueError(
                "Axiom must be included in the set of non terminals.",
            )

        if non_terminals != set(productions.keys()):
            raise ValueError(
                f"Set of non-terminals and productions keys should be equal."
            )

        for nt, rhs in productions.items():
            if not rhs:
                raise ValueError(
                    f"No production rules for non terminal symbol {nt} "
                )
            for r in rhs:
                for s in r:
                    if (
                        s not in non_terminals
                        and s not in terminals
                    ):
                        raise ValueError(
                            f"Invalid symbol {s}.",
                        )

        self.terminals = terminals
        self.non_terminals = non_terminals
        self.productions = productions
        self.axiom = axiom
        self._first_sets = self.compute_first_sets()
        self._follow_sets = self.compute_follow_sets()


    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"axiom={self.axiom!r}, "
            f"productions={self.productions!r})"
        )


    def compute_first_sets(self) -> Dict[str, AbstractSet[str]]:
        all_first: Dict[str, AbstractSet[str]] = {nt: set() for nt in self.non_terminals}

        # Inicialización: si A -> '' entonces '' in FIRST(A).
        # Si A -> a... donde a es terminal, a pertenece a FIRST(A).
        for A in self.non_terminals:
            for prod in self.productions[A]:
                if prod == "":
                    all_first[A].add("")
                elif len(prod) > 0 and prod[0] in self.terminals:
                    all_first[A].add(prod[0])

        changed = True
        while changed:
            changed = False
            for A in self.non_terminals:
                for prod in self.productions[A]:
                    if prod == "":
                        if "" not in all_first[A]:
                            all_first[A].add("")
                            changed = True
                        continue

                    add_eps = True
                    for X in prod:
                        if X in self.terminals:
                            if X not in all_first[A]:
                                all_first[A].add(X)
                                changed = True
                            add_eps = False
                            break
                        else:
                            before = len(all_first[A])
                            all_first[A].update(all_first[X] - {""})
                            if len(all_first[A]) != before:
                                changed = True
                            if "" in all_first[X]:
                                continue
                            else:
                                add_eps = False
                                break

                    if add_eps:
                        if "" not in all_first[A]:
                            all_first[A].add("")
                            changed = True

        return all_first

    def compute_first(self, sentence: str) -> AbstractSet[str]:
        """
        Method to compute the first set of a string.

        Args:
            str: string whose first set is to be computed.

        Returns:
            First set of str.
        """

	    # TO-DO: Complete this method for exercise 3...
        for sy in sentence:
            if sy not in self.terminals and sy not in self.non_terminals:
                raise ValueError ("El caracter no esta en el lenguaje")

        if sentence == "":
            return {''}

        if sentence[0] in self.terminals:
            return set(sentence[0])

        return_set = set()
        for i, sy in enumerate(sentence):

            # obtener los primeros de su produccion
            if sy in self.non_terminals:

                sy_set = self._first_sets[sy]
                return_set.update(sy_set - {''})

                # si no puede procesar lambda, ahi se queda
                if "" not in sy_set:
                    break
            elif sy in self.terminals:
                # paramos porque ya hay un primero
                return_set.add(sy)
                break

            # en caso de que sea el último
            if i == len(sentence) - 1:
                return_set.add('')

        return return_set

    def compute_follow_sets(self) -> Dict[str, AbstractSet[str]]:
        all_follow = dict()

        for non_terminal in self.non_terminals:
            all_follow[non_terminal] = set()

        # 1. Añadir $ al axioma
        all_follow[self.axiom].add("$")

        return_follow = {nt: set() for nt in self.non_terminals}
        return_follow[self.axiom].add('$')

        flag = True
        while flag:
            # copiamos los valores, PROBLEMAS COPIANDO SINO
            prev_follow = copy.deepcopy(return_follow)
            # A -> (alfa)(X)(beta)
            for alfa, productions in self.productions.items():
                for prod in productions:
                    for i, sy in enumerate(prod):
                        if sy in self.non_terminals:
                            # SIG(X) += PR(B) - lambda, no contempla el ultimo caso
                            if i + 1 < len(prod):
                                next_first = self.compute_first(prod[i + 1:])
                                return_follow[sy].update(next_first - {""})

                            # Último símbolo o el PR del siguiente contiene lambda, agregar SIG de alfa
                            if i == len(prod) - 1 or (i + 1 < len(prod) and "" in self.compute_first(prod[i + 1:])):
                                return_follow[sy].update(return_follow[alfa])

            if prev_follow == return_follow:
                flag = False

        return return_follow

    def compute_follow(self, symbol: str) -> AbstractSet[str]:
        """
        Method to compute the follow set of a non-terminal symbol.

        Args:
            symbol: non-terminal whose follow set is to be computed.

        Returns:
            Follow set of symbol.
        """

	# TO-DO: Complete this method for exercise 4...
        if symbol not in self.non_terminals:
            raise ValueError ("El simbolo no es un no terminal")
        return self._follow_sets[symbol]

    def get_ll1_table(self) -> Optional[LL1Table]:
        """
        Method to compute the LL(1) table.

        Returns:
            LL(1) table for the grammar, or None if the grammar is not LL(1).
        """

	# TO-DO: Complete this method for exercise 5...
        terminales = self.terminals.union({'$'})

        tabla = LL1Table(self.non_terminals, terminales)

        try:
            for non_terminal in self.non_terminals:
                for prod in self.productions[non_terminal]:
                    set_primeros = self.compute_first(prod)

                    if '' in set_primeros:
                        set_primeros = set_primeros - {''}
                        set_siguientes = self.compute_follow(non_terminal)
                        for symbol in set_siguientes:
                            tabla.add_cell(non_terminal, symbol, prod)

                    for terminal in set_primeros:
                        tabla.add_cell(non_terminal, terminal, prod)

        except RepeatedCellError:
            # Si hay conflicto en la tabla, la gramática no es LL(1)
            return None

        return tabla


    def is_ll1(self) -> bool:
        return self.get_ll1_table() is not None


class LL1Table:
    """
    LL1 table. Initially all cells are set to None (empty). Table cells
    must be filled by calling the method add_cell.

    Args:
        non_terminals: Set of non terminal symbols.
        terminals: Set of terminal symbols.

    """

    def __init__(
        self,
        non_terminals: AbstractSet[str],
        terminals: AbstractSet[str],
    ) -> None:

        if terminals & non_terminals:
            raise ValueError(
                "Intersection between terminals and non terminals "
                "must be empty.",
            )

        self.terminals: AbstractSet[str] = terminals
        self.non_terminals: AbstractSet[str] = non_terminals
        self.cells: Dict[str, Dict[str, Optional[str]]] = {nt: {t: None for t in terminals} for nt in non_terminals}

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"cells={self.cells!r})"
        )

    def add_cell(self, non_terminal: str, terminal: str, cell_body: str) -> None:
        """
        Adds a cell to an LL(1) table.

        Args:
            non_terminal: Non termial symbol (row)
            terminal: Terminal symbol (column)
            cell_body: content of the cell

        Raises:
            RepeatedCellError: if trying to add a cell already filled.
        """
        if non_terminal not in self.non_terminals:
            raise ValueError(
                "Trying to add cell for non terminal symbol not included "
                "in table.",
            )
        if terminal not in self.terminals:
            raise ValueError(
                "Trying to add cell for terminal symbol not included "
                "in table.",
            )
        if not all(x in self.terminals | self.non_terminals for x in cell_body):
            raise ValueError(
                "Trying to add cell whose body contains elements that are "
                "not either terminals nor non terminals.",
            )
        if self.cells[non_terminal][terminal] is not None:
            raise RepeatedCellError(
                f"Repeated cell ({non_terminal}, {terminal}).")
        else:
            self.cells[non_terminal][terminal] = cell_body

    def analyze(self, input_string: str, start: str) -> ParseTree:
        """
        Method to analyze a string using the LL(1) table.

        Args:
            input_string: string to analyze.
            start: initial symbol.

        Returns:
            ParseTree object with either the parse tree (if the elective exercise is solved)
            or an empty tree (if the elective exercise is not considered).

        Raises:
            SyntaxError: if the input string is not syntactically correct.
        """

        arbol = ParseTree(start)

        # pila_nodos: deque usado como **pila**
        pila_nodos = deque([arbol, ParseTree("$")])
        # buffer_entrada: deque usado como **cola**
        buffer_entrada = deque(input_string)

        while pila_nodos and buffer_entrada:
            # 1. Extraer el primer nodo (tope de la pila: left end)
            nodo_pila = pila_nodos.popleft()
            simbolo_entrada = buffer_entrada.popleft()

            if simbolo_entrada not in self.terminals:
                raise SyntaxError("Terminal no forma parte del lenguaje.")

            # 1a. Si el nodo de la pila es un no terminal, buscamos la producción en la tabla
            if nodo_pila.root in self.non_terminals:

                entrada_tabla = self.cells[nodo_pila.root][simbolo_entrada]

                # Si no hay entrada en la tabla, error sintáctico
                if entrada_tabla is None:
                    raise SyntaxError(f"Cadena no válida (no hay celda para ({nodo_pila.root}, {simbolo_entrada}))")

                # Si hay producción distinta de λ
                if entrada_tabla and entrada_tabla != '':
                    produccion = entrada_tabla
                    hijos = [ParseTree(sim) for sim in produccion]
                    nodo_pila.add_children(hijos)

                    # Añadir hijos al **tope** de la pila (appendleft), en orden inverso
                    for hijo in reversed(hijos):
                        pila_nodos.appendleft(hijo)

                    # Devolvemos el símbolo al buffer porque aún no lo hemos consumido
                    buffer_entrada.appendleft(simbolo_entrada)

                # Si la producción es λ
                elif entrada_tabla == '':
                    # Añadir un hijo λ para representar la producción vacía
                    nodo_pila.add_children([ParseTree("λ")])
                    buffer_entrada.appendleft(simbolo_entrada)

            # 1b. Si el nodo de la pila es un terminal, debe coincidir con la entrada
            elif nodo_pila.root in self.terminals:
                if nodo_pila.root == simbolo_entrada:
                    # terminal correcto: continuar
                    pass
                else:
                    raise SyntaxError(f"Cadena no válida (terminal en pila '{nodo_pila.root}' != entrada '{simbolo_entrada}')")

        # Si queda algo sin procesar, error sintáctico
        if pila_nodos or buffer_entrada:
            raise SyntaxError('Cadena no válida')

        return arbol





class ParseTree():
    """
    Parse Tree.

    Args:
        root: root node of the tree.
        children: list of children, which are also ParseTree objects.
    """
    def __init__(self, root: str, children: Optional[Collection[ParseTree]] = None) -> None:
        self.root = root
        # Evitar valor por defecto mutable compartido
        self.children = list(children) if children is not None else []

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.root!r}: {self.children})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.root == other.root
            and len(self.children) == len(other.children)
            and all([x.__eq__(y) for x, y in zip(self.children, other.children)])
        )

    def add_children(self, children: Collection[ParseTree]) -> None:
        self.children = children
