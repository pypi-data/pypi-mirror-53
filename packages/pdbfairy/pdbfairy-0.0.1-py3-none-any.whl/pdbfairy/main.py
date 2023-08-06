import collections
import math
import os
import sys

from Bio import PDB
import memoized
from numpy import linalg
import numpy


MAX_DISTANCE = 4


def print_interactions(structure, max_distance):
    atom_pairs = find_pairs(structure, max_distance)
    res_pairs = set()
    for atom_1, atom_2 in atom_pairs:
        res_pairs.add((atom_1.parent, atom_2.parent))

    print("PDB file name\t{}".format(structure.id))
    print("Distance cutoff\t{}".format(max_distance))
    print()
    print()
    print()
    print("Chain\tResidue number\tChain\tResidue number")

    lines = []

    def get_line(res_1, res_2):
        return (get_res_chain(res_1), get_res_number(res_1),
                get_res_chain(res_2), get_res_number(res_2))

    for res_1, res_2 in res_pairs:
        lines.append(get_line(res_1, res_2))
        lines.append(get_line(res_2, res_1))
    lines.sort()
    for line in lines:
        print('{}\t{}\t{}\t{}'.format(*line))


def find_pairs(structure, max_distance=MAX_DISTANCE):
    atoms = list(structure.get_atoms())
    atom_store = AtomStore(atoms, max_distance=max_distance)
    for atom in atoms:
        yield from atom_store.find_neighbors(atom)
        atom_store.remove(atom)


class AtomStore(object):
    def __init__(self, atoms=(), max_distance=MAX_DISTANCE):
        # max distance for two atoms to be considered "neighbors"
        self.max_distance = max_distance
        self._atoms_by_cube = collections.defaultdict(set)
        self._atoms_by_chain = collections.defaultdict(set)
        for atom in atoms:
            self.add(atom)

    def add(self, atom):
        self._atoms_by_cube[tuple(self._get_cube(atom))].add(atom)
        self._atoms_by_chain[self._get_chain(atom)].add(atom)

    def remove(self, atom):
        self._atoms_by_cube[tuple(self._get_cube(atom))].remove(atom)
        self._atoms_by_chain[self._get_chain(atom)].remove(atom)

    def find_neighbors(self, atom):
        cube = self._get_cube(atom)
        atoms_in_chain = self._atoms_by_chain[self._get_chain(atom)]
        yield from (
            (atom, a)
            for offset in self._offsets
            for a in self._atoms_by_cube[tuple(cube + offset)] - atoms_in_chain
            if dist(a, atom) <= self.max_distance
        )

    @memoized.memoized
    def _get_cube(self, atom):
        return numpy.floor(atom.coord / self.max_distance)

    @memoized.memoized
    def _get_chain(self, atom):
        return atom.parent.parent

    _offsets = [
        numpy.array([i, j, k])
        for i in [-1, 0, 1]
        for j in [-1, 0, 1]
        for k in [-1, 0, 1]
    ]


def dist(atom_1, atom_2):
    return linalg.norm(atom_1.coord - atom_2.coord)


def get_res_chain(res):
    return res.parent.id


def get_res_number(res):
    return res.id[1]

def main():
    pdb_file = sys.argv[1]
    try:
        max_distance = float(sys.argv[2])
    except IndexError:
        max_distance = MAX_DISTANCE
    parser = PDB.PDBParser()
    pdb_name = ''.join(os.path.splitext(os.path.basename(pdb_file))[:-1])
    structure = parser.get_structure(pdb_name, pdb_file)
    print_interactions(structure, max_distance)


if __name__ == '__main__':
    main()