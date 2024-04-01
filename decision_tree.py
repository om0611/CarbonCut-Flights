from __future__ import annotations

import csv
from typing import Any, Optional


class Tree:
    """
    A recursive tree data structure.
    """

    _root: Optional[Any]
    _subtrees: list[Tree]

    def __init__(self, root: Optional[Any], subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return whether this tree is empty.

        """
        return self._root is None

    def __len__(self) -> int:
        """Return the number of items contained in this tree.
        """
        if self.is_empty():
            return 0
        else:
            size = 1
            for subtree in self._subtrees:
                size += subtree.__len__()
            return size

    def __contains__(self, item: Any) -> bool:
        """Return whether the given is in this tree.

        """
        if self.is_empty():
            return False
        elif self._root == item:
            return True
        else:
            for subtree in self._subtrees:
                if subtree.__contains__(item):
                    return True
            return False

    def traverse(self, path: list[bool]) -> list[Any]:
        """
        This function traverses a decision tree and returna all the leafs at the end of a given path.
        """
        if self.is_empty():
            return []

        if not path:
            leaves = []
            for subtree in self._subtrees:
                leaves.extend([subtree._root])
            return leaves

        direction = path[0]
        next_path = path[1:]

        for subtree in self._subtrees:
            if subtree._root == direction:
                return subtree.traverse(next_path)

        return []

    def create_tree(self, items: list) -> Tree:
        """
        Create a tree from the provided list, ensuring that each subsequent item is a child of the previous.
        Preconditions:
            - self.is_empty()
        """
        root = items[0]
        subtrees = []
        if len(items) > 1:
            subtree = self.create_tree(items[1:])
            subtrees.append(subtree)

        return Tree(root, subtrees)

    def insert_sequence(self, items: list) -> None:
        """
        Insert the given items into this tree.

        """
        if not items:
            return
        elif not self._subtrees:
            empty_tree = Tree(None, [])
            self._subtrees.append(empty_tree.create_tree(items))
            return
        else:
            root = items[0]
            rest_items = items[1:]
            for subtree in self._subtrees:
                if subtree._root == root:
                    subtree.insert_sequence(rest_items)
                    return

            empty_tree = Tree(None, [])
            self._subtrees.append(empty_tree.create_tree(items))
            return


def build_decision_tree(file: str) -> Tree:
    """
    Build a decision tree storing the country data from the given file.
    """
    tree = Tree('', [])

    with open(file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            values = [False if x == 'No' else True for x in row[1:]]
            tree.insert_sequence(values + [row[0]])

    return tree


def get_user_input(questions: list[str]) -> list[bool]:
    """Return the user's answers to a list of Yes/No questions."""
    answers_so_far = []

    for question in questions:
        print(question)
        s = input('Y/N: ')
        answers_so_far.append(s == 'Y')  # Any other input is interpreted as False

    return answers_so_far


TRAVEL_QUESTIONS = [
    'Do you prefer a vacation in a climate that is primarily warm and sunny, rather than cold?',
    'Would you like to be near beaches, lakes, rivers?',
    'Are you looking for destinations where you can engage in outdoor activities, such as hiking, '
    'skiing, or wildlife watching?',
    'Do you prefer a destination that offers a vibrant nightlife?',
]


def run_country_matchmaker(file: str) -> None:
    """Run a country matching program based on the given file.
    """
    decision_tree = build_decision_tree(file)
    char = get_user_input(TRAVEL_QUESTIONS)
    matches = decision_tree.traverse(char)
    if not matches:
        print("There are no countries with this match.")
    else:
        print(f"The following country(s) match your inputs: {matches}")


def all_countries(flight_path_file: str) -> tuple[set[str], set[str]]:
    destination_countries = set()
    original_countries = set()
    with open(flight_path_file, mode='r') as flight_paths:
        reader = csv.reader(flight_paths)
        next(flight_paths)
        for row in reader:
            original_countries.add(row[1])
            destination_countries.add(row[3])

    return (original_countries, destination_countries)
