from csp import Constraint, CSP
from typing import Dict, List, Optional

class QueensConstraint(Constraint[int, int]):
    def __init__(self, columns: List) -> None:
        super().__init__(columns)
        self.columns: List[int] = columns

    def satisfied(self, assignment: Dict[int, int]) -> bool:
        for q1c, q1r in assignment.items():
            for q2c in range(q1c+1, len(self.columns)+1):
                if q2c in assignment:
                    q2r = assignment[q2c]
                    if q1r == q2r:
                        return False
                    if abs(q1c - q2c) == abs(q1r - q2r):
                        return False
        return True

def print_queen(queen: Dict[int, int]):
    print()
    localqueen = sorted(queen.items(), key=lambda kv: (kv[1]))
    for col, row in localqueen:
        print('+\t' * (col - 1) + '♚\t' + '+\t' * (8 - col))
    print("\n\n")

if __name__== "__main__":
    columns: List[int] = [1, 2, 3, 4, 5, 6, 7, 8]
    rows: Dict[int, List[int]] = {}
    for column in columns:
        rows[column] = [1, 2, 3, 4, 5, 6, 7, 8]
    csp: CSP[int, int]= CSP(columns, rows)
    csp.add_constraint(QueensConstraint(columns))
    csp.show_constraints()

    solution: Optional[Dict[int, int]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        print_queen(solution)