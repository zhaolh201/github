
from typing import TypeVar, Generic, Dict, List, Optional
from abc import ABC, abstractmethod
from log import *

V = TypeVar('V')
D = TypeVar('D')

class Constraint(Generic[V, D], ABC):
    def __init__(self, variables: List[V]) -> None:
        self.variables = variables

    def __str__(self) ->str:
        return f"{self.variables}"

    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> bool:
        ...

class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        self.variables: List[V] = variables
        self.domains: Dict[V, List[D]] = domains
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Every variable should have a domain assigned to it.")

    def add_constraint(self, constraint: Constraint[V, D]) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)

    def show_constraints(self) -> None:
        print('CSP Constraints:')
        print('{')
        for variable1 in self.constraints:
            result = f"{variable1}:"
            if self.constraints[variable1]:
                result += '['
                for j in range(len(self.constraints[variable1])):
                    result += f"{self.constraints[variable1][j]}"
                    if j != len(self.constraints[variable1]) - 1:
                        result += ','
                result += ']'
            else:
                result += '[]'
            print(result)
        print('}')

    def consistent(self, variable: V, assignment: Dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                print(f"Variable {variable} value {assignment[variable]} ne satisfied pas {constraint}")
                return False
        print(f"Variable {variable} value {assignment[variable]} satisfied all constraints")
        return True

    # @fonction_log
    def backtracking_search(self, assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
        print('assignment:', assignment)

        if len(assignment) == len(self.variables):
            return assignment

        unassigned: List[V] = [v for v in self.variables if v not in assignment]
        first: V = unassigned[0]
        print(f"Variables n'attribuer pas: {unassigned} parcourir {first} !")

        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            if self.consistent(first, local_assignment):
                result: Optional[Dict[V, D]] = self.backtracking_search(local_assignment)
                # if we didn't find the result, we will end up backtracking
                if result is not None:
                    return result
        return None










