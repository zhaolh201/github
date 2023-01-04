# csp.py
# From Classic Computer Science Problems in Python Chapter 3
# Copyright 2018 David Kopec
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Generic, TypeVar, Dict, List, Optional
from abc import ABC, abstractmethod
from queens_v2 import QueensConstraint

V = TypeVar('V') # variable type
D = TypeVar('D') # domain type

# Base class for all constraints
# Classe abstrait
class Constraint(Generic[V, D], ABC):
    # The variables that the constraint is between//Les variables entre lesquelles se situe la contrainte
    # Constructeur abstrait comme modèle
    def __init__(self, variables: List[V]) -> None:
        """
            >>> csp = CSP([1, 2, 3, 4],{1: [1, 2, 3, 4], 2: [1, 2, 3, 4], 3: [1, 2, 3, 4], 4: [1, 2, 3, 4]})
            >>> csp.variables
            [1, 2, 3, 4]
            >>> csp2 = CSP([1, 2, 3, 4, 5],{1: [1, 2, 3, 4, 5], 2: [1, 2, 3, 4, 5], 3: [1, 2, 3, 4, 5], 4: [1, 2, 3, 4, 5], 5: [1, 2, 3, 4, 5]})
            >>> csp2.variables
            [1, 2, 3, 4, 5]
        """
        # Les classes de base abstraites servent de modèles pour une hiérarchie de classes.
        # Le modèle oblige l'emploi de cet attribut
        self.variables = variables

    # Must be overridden by subclasses//Doit être remplacé par les sous-classes
    # Méthode abstrainte comme modèle
    # qui oblige l'emploi de cette méthode
    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> bool:
        ...


# A constraint satisfaction problem consists of variables of type V
# that have ranges of values known as domains of type D and constraints
# that determine whether a particular variable's domain selection is valid
# Un problème de satisfaction de contraintes est constitué de variables de type V
# qui ont des plages de valeurs appelées domaines de type D et des contraintes
# qui déterminent si la sélection de domaine d'une variable particulière est valide
class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        """
            >>> csp = CSP([1, 2, 3, 4],{1: [1, 2, 3, 4], 2: [1, 2, 3, 4], 3: [1, 2, 3, 4], 4: [1, 2, 3, 4]})
            >>> csp2 = CSP([1, 2, 3, 4, 5],{1: [1, 2, 3, 4, 5], 2: [1, 2, 3, 4, 5], 3: [1, 2, 3, 4, 5], 4: [1, 2, 3, 4, 5], 5: [1, 2, 3, 4, 5]})
            >>> csp.variables
            [1, 2, 3, 4]
            >>> csp2.variables
            [1, 2, 3, 4, 5]
            >>> csp.domains
            {1: [1, 2, 3, 4], 2: [1, 2, 3, 4], 3: [1, 2, 3, 4], 4: [1, 2, 3, 4]}
            >>> csp2.domains
            {1: [1, 2, 3, 4, 5], 2: [1, 2, 3, 4, 5], 3: [1, 2, 3, 4, 5], 4: [1, 2, 3, 4, 5], 5: [1, 2, 3, 4, 5]}
            >>> csp.constraints
            {1: [], 2: [], 3: [], 4: []}
            >>> csp2.constraints
            {1: [], 2: [], 3: [], 4: [], 5: []}
        """

        # L'initialiseur __init__() crée les contraintes dict. La add_constraint()
        # la méthode passe par toutes les variables touchées par une contrainte donnée et s'ajoute à
        # la cartographie des contraintes pour chacun d'eux. Les deux méthodes ont une vérification des erreurs de base dans
        # lieu et lèvera une exception lorsqu'il manque un domaine ou une contrainte à une variable
        # est sur une variable inexistante.

        self.variables: List[V] = variables # variables to be constrained
        self.domains: Dict[V, List[D]] = domains # domain of each variable
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        # Valider que chaque variable est dans le domaine
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Every variable should have a domain assigned to it.")

    def add_constraint(self, constraint: Constraint[V, D]) -> None:
        """
            >>> csp = CSP([1, 2, 3, 4],{1: [1, 2, 3, 4], 2: [1, 2, 3, 4], 3: [1, 2, 3, 4], 4: [1, 2, 3, 4]})
            >>> csp2 = CSP([1, 2, 3, 4, 5],{1: [1, 2, 3, 4, 5], 2: [1, 2, 3, 4, 5], 3: [1, 2, 3, 4, 5], 4: [1, 2, 3, 4, 5], 5: [1, 2, 3, 4, 5]})
            >>> cols: List[int] = [1, 2, 3, 4]
            >>> cols2: List[int] = [1, 2, 3, 4, 5]
            >>> csp.add_constraint(QueensConstraint(cols))
            >>> len(csp.constraints)
            4
            >>> csp2.add_constraint(QueensConstraint(cols2))
            5


        """

        # Selon la liste vide construite dans la validation dans __init__
        for variable in constraint.variables:
            # Valider une 2e fois
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            # Ajouter (si la validation est bonne)
            # la contrainte dans la liste construire dans __init__
            else:
                self.constraints[variable].append(constraint)


    # Check if the value assignment is consistent by checking all constraints
    # for the given variable against it
    # Vérifier si l'affectation de valeur est cohérente en vérifiant toutes les contraintes
    # pour la variable donnée contre elle
    def consistent(self, variable: V, assignment: Dict[V, D]) -> bool:
        """
            >>> csp = CSP([1, 2, 3, 4],{1: [1, 2, 3, 4], 2: [1, 2, 3, 4], 3: [1, 2, 3, 4], 4: [1, 2, 3, 4]})
            >>> csp.constraints
            {1: [], 2: [], 3: [], 4: []}
            >>> csp2 = CSP([1, 2, 3, 4, 5],{1: [1, 2, 3, 4, 5], 2: [1, 2, 3, 4, 5], 3: [1, 2, 3, 4, 5], 4: [1, 2, 3, 4, 5], 5: [1, 2, 3, 4, 5]})
            >>> csp2.constraints
            {1: [], 2: [], 3: [], 4: [], 5: []}
        """
        # consistent() parcourt toutes les contraintes pour une variable donnée (ce sera toujours la
        # variable qui vient d'être ajoutée à l'affectation) et vérifie si la contrainte est satisfaite,
        # étant donné la nouvelle affectation. Si l'affectation satisfait toutes les contraintes, True vaut
        # revenu. Si une contrainte imposée à la variable n'est pas satisfaite, False est renvoyé.
        # Ce cadre de satisfaction de contraintes utilisera une simple recherche de retour en arrière pour trouver
        # solutions aux problèmes. Le retour en arrière est l'idée qu'une fois que vous avez atteint un mur dans votre
        # recherche, vous revenez au dernier point connu où vous avez pris une décision avant le mur, et choisissez
        # un chemin différent.
        for constraint in self.constraints[variable]:
            print("constraint,", constraint, "; variable (col),", variable, "; assigné, {col: ran}", assignment)
            if not constraint.satisfied(assignment):
                return False
        return True

    def backtracking_search(self, assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
        """
            >>> csp = CSP([1, 2, 3, 4],{1: [1, 2, 3, 4], 2: [1, 2, 3, 4], 3: [1, 2, 3, 4], 4: [1, 2, 3, 4]})
            >>> csp2 = CSP([1, 2, 3, 4, 5],{1: [1, 2, 3, 4, 5], 2: [1, 2, 3, 4, 5], 3: [1, 2, 3, 4, 5], 4: [1, 2, 3, 4, 5], 5: [1, 2, 3, 4, 5]})

            assert csp.backtracking_search() == {1: 2, 2: 4, 3: 1, 4: 3}
            assert csp2.backtracking_search() == {1: 1, 2: 3, 3: 5, 4: 2, 5: 4}
        """
        # assignment is complete if every variable is assigned (our base case)
        # l'affectation est complète si chaque variable est affectée(notre cas de base)
        print("assigné, {col: ran},", assignment, end="; ")
        if len(assignment) == len(self.variables):
            return assignment

        # get all variables in the CSP but not in the assignment
        # obtenir toutes les variables dans le CSP mais pas dans l'affectation
        unassigned: List[V] = [v for v in self.variables if v not in assignment]
        print("non assigné, [col]", unassigned)
        
        # get the every possible domain value of the first unassigned variable
        # obtenir toutes les valeurs de domaine possibles de la première variable non affectée

        first: V = unassigned[0]
        
        for value in self.domains[first]:
            print("valeur du domaine (ran),", value)
            local_assignment = assignment.copy()
            local_assignment[first] = value
            print("assigné local, {col: ran},", local_assignment)
            # if we're still consistent, we recurse (continue)
            print("consistent,", self.consistent(first, local_assignment))
            if self.consistent(first, local_assignment): # if True
                result: Optional[Dict[V, D]] = self.backtracking_search(local_assignment)
                # if we didn't find the result, we will end up backtracking
                if result is not None:
                    return result
        return None


    def backtracking_search_2(self, assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
        """
            # >>> csp = CSP([1, 2, 3, 4],{1: [1, 2, 3, 4], 2: [1, 2, 3, 4], 3: [1, 2, 3, 4], 4: [1, 2, 3, 4]})
            # >>> csp2 = CSP([1, 2, 3, 4, 5],{1: [1, 2, 3, 4, 5], 2: [1, 2, 3, 4, 5], 3: [1, 2, 3, 4, 5], 4: [1, 2, 3, 4, 5], 5: [1, 2, 3, 4, 5]})
            # assert csp.consistent(1, {1: 2, 2: 2, 3: 1, 4: 3}) == False
            # assert csp2.consistent(1, {1: 5, 2: 3, 3: 1, 4: 4, 5: 2}) == True
            # assert csp2.consistent(1, {1: 4, 2: 1, 3: 5, 4: 2, 5: 3}) == False
        """
        """"Appliquer un algorithme au problème; déterminer
        les variables non assignées et
        choisir la 2e des variables non assignées
        selon l'ordre statique"""
        # assignment is complete if every variable is assigned (our base case)
        print("assigné, {col: ran},", assignment, end="; ")
        if len(assignment) == len(self.variables):
            return assignment

        # get all variables in the CSP but not in the assignment
        unassigned: List[V] = [v for v in self.variables if v not in assignment]
        print("non assigné, [col]", unassigned)

        # get the every possible domain value of the first unassigned variable
        first: V = unassigned[1]

        for value in self.domains[first]:
            print("valeur du domaine (ran),", value)
            local_assignment = assignment.copy()
            local_assignment[first] = value
            print("assigné local, {col: ran},", local_assignment)
            # if we're still consistent, we recurse (continue)
            print("consistent,", self.consistent(first, local_assignment))
            if self.consistent(first, local_assignment):  # if True
                result: Optional[Dict[V, D]] = self.backtracking_search(local_assignment)
                # if we didn't find the result, we will end up backtracking
                if result is not None:
                    return result
        return None
