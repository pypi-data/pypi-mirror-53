#!/usr/bin/env python3

# TODO Add remaining xml methods for Protein class

from QUBEKit.engines import RDKit, Element
from QUBEKit.utils import constants
from QUBEKit.utils.exceptions import FileTypeError, TopologyMismatch

from collections import OrderedDict
from datetime import datetime
from itertools import groupby
import os
from pathlib import Path
import pickle
import re

import networkx as nx
import numpy as np

import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString


class Atom:
    """
    Class to hold all of the "per atom" information.
    All atoms in Molecule will have an instance of this Atom class to describe their properties.
    """

    def __init__(self, atomic_number, atom_index, atom_name='', partial_charge=None, formal_charge=None):

        self.atomic_number = atomic_number
        # The actual atomic name as per periodic table e.g. C, F, Pb, etc
        self.atomic_mass = Element().mass(atomic_number)
        self.atomic_symbol = Element().name(atomic_number).title()
        # The QUBEKit assigned name derived from the atomic name and its index e.g. C1, F8, etc
        self.atom_name = atom_name
        self.atom_index = atom_index
        self.partial_charge = partial_charge
        self.formal_charge = formal_charge
        self.atom_type = None
        self.bonds = []

    def add_bond(self, bonded_index):
        """
        Add a bond to the atom, this will make sure the bond has not already been described
        :param bonded_index: The index of the atom bonded to self
        """

        if bonded_index not in self.bonds:
            self.bonds.append(bonded_index)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__dict__!r})'

    def __str__(self):
        """
        Prints the Atom class objects' names and values one after another with new lines between each.
        """

        return_str = ''
        for key, val in self.__dict__.items():
            # Return all objects as {atom object name} = {atom object value(s)}.
            return_str += f'\n{key} = {val}\n'

        return return_str


class DefaultsMixin:
    """
    This class holds all of the default configs from the config file.
    It's effectively a placeholder for all of the attributes which may
    be changed by editing the config file(s).

    It's a mixin because:
        * Normal multiple inheritance doesn't make sense in this context
        * Composition would be a bit messier and may require stuff like:
            mol = Ligand('methane.pdb', 'methane')
            mol.defaults.threads
            >> 2

            rather than the nice clean:
            mol.threads
            >> 2
        * Mixin is cleaner and clearer with respect to super() calls.
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.theory = 'wB97XD'
        self.basis = '6-311++G(d,p)'
        self.vib_scaling = 1
        self.threads = 2
        self.memory = 2
        self.convergence = 'GAU_TIGHT'
        self.iterations = 350
        self.bonds_engine = 'psi4'
        self.density_engine = 'g09'
        self.charges_engine = 'chargemol'
        self.ddec_version = 6
        self.geometric = True
        self.solvent = True

        self.dih_start = -165
        self.increment = 15
        self.dih_end = 180
        self.t_weight = 'infinity'
        self.opt_method = 'BFGS'
        self.refinement_method = 'SP'
        self.tor_limit = 20
        self.div_index = 0
        self.parameter_engine = 'xml'
        self.l_pen = 0.0
        self.mm_opt_method = 'openmm'
        self.relative_to_global = False

        self.excited_state = False
        self.excited_theory = 'TDA'
        self.nstates = 3
        self.excited_root = 1
        self.use_pseudo = False
        self.pseudo_potential_block = ""

        self.chargemol = '/home/<QUBEKit_user>/chargemol_09_26_2017'
        self.log = 999


class Molecule:
    """Base class for ligands and proteins."""

    def __init__(self, mol_input, name=None):
        """
        # Namings
        smiles                  str; SMILES string for the molecule e.g. 'c1cc[nH]c1'
        filename                str; Full filename e.g. methane.pdb
        qc_json                 json dict; QC json data. Only used if loading from qcarchive/portal
        name                    str; Molecule name e.g. 'methane'

        # Structure
        coords                  Dict of numpy arrays of the coords where the keys are the input type ('mm', 'qm', etc)
        topology                networkx Graph() object. Contains connection information for molecule
        angles                  List of tuples; Shows angles based on atom indices (from 0) e.g. (1, 2, 4), (1, 2, 5)
        dihedrals               Dictionary of dihedral tuples stored under their common core bond
                                e.g. {(1,2): [(3, 1, 2, 6), (3, 1, 2, 7)]}
        improper_torsions
        rotatable               List of dihedral core tuples [(1,2)]
        bond_lengths            Dictionary of bond lengths stored under the bond tuple
                                e.g. {(1, 3): 1.115341203992107} (angstroms)
        dih_phis                Dictionary of the dihedral angles measured in the molecule object stored under the
                                dihedral tuple e.g. {(3, 1, 2, 6): -70.3506776877}  (degrees)
        angle_values            Dictionary of the angle values measured in the molecule object stored under the
                                angle tuple e.g. {(2, 1, 3): 107.2268} (degrees)
        symm_hs
        qm_energy

        # XML Info
        xml_tree                An XML class object containing the force field values
        AtomTypes               dict of lists; basic non-symmetrised atoms types for each atom in the molecule
                                e.g. {0, ['C1', 'opls_800', 'C800'], 1: ['H1', 'opls_801', 'H801'], ... }
        Residues                List of residue names in the sequence they are found in the protein
        extra_sites
        qm_scans                Dictionary of central scanned bonds and there energies and structures

        Parameters
        -------------------
        This section has different units due to it interacting with OpenMM

        HarmonicBondForce       Dictionary of equilibrium distances and force constants stored under the bond tuple.
                                {(1, 2): [0.108, 405.65]} (nano meters, kJ/mol)
        HarmonicAngleForce      Dictionary of equilibrium angles and force constants stored under the angle tuple
                                e.g. {(2, 1, 3): [2.094395, 150.00]} (radians, kJ/mol)
        PeriodicTorsionForce    Dictionary of lists of the torsions values [periodicity, k, phase] stored under the
                                dihedral tuple with an improper tag only for improper torsions
                                e.g. {(3, 1, 2, 6): [[1, 0.6, 0], [2, 0, 3.141592653589793], ... Improper]}
        NonbondedForce          OrderedDict; L-J params. Keys are atom index, vals are [charge, sigma, epsilon]

        combination             str; Combination rules e.g. 'opls'
        sites                   OrderedDict of virtual site parameters
                                e.g.{0: [(top nos parent, a .b), (p1, p2, p3), charge]}

        # QUBEKit Internals
        state                   str; Describes the stage the analysis is in for pickling and unpickling
        config_file             str or path; the config file used for the execution
        restart                 bool; is the current execution starting from the beginning (False) or restarting (True)?
        """

        self.mol_input = mol_input
        self.name = name

        # The three possible input types; these are set in read_input()
        self.filename = None
        self.smiles = None
        self.qc_json = None

        self.rdkit_mol = None

        # Structure
        self.coords = {'qm': [], 'mm': [], 'input': [], 'temp': [], 'traj': []}
        self.topology = None
        self.angles = None
        self.dihedrals = None
        self.improper_torsions = None
        self.rotatable = None
        self.bond_lengths = None
        self.atoms = None
        self.dih_phis = None
        self.angle_values = None
        self.symm_hs = None
        self.qm_energy = None
        self.charge = 0
        self.multiplicity = 1
        self.qm_scans = None
        self.scan_order = None
        self.descriptors = None

        # XML Info
        self.xml_tree = None
        self.AtomTypes = None
        self.Residues = None
        self.extra_sites = None
        self.HarmonicBondForce = None
        self.HarmonicAngleForce = None
        self.PeriodicTorsionForce = None
        self.NonbondedForce = None
        self.bond_types = None
        self.angle_types = None
        self.dihedral_types = None

        self.combination = None
        self.sites = None

        # QUBEKit internals
        self.state = None
        self.config_file = 'master_config.ini'
        self.restart = False
        self.atom_symmetry_classes = None
        self.verbose = True

        # Read mol_input and generate mol info from file, smiles string or qc_json.
        self.read_input()
        self.check_names_are_unique()

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__dict__!r})'

    def __str__(self, trunc=False):
        """
        Prints the Molecule class objects' names and values one after another with new lines between each.
        Mostly just used for logging, debugging and displaying the results at the end of a run.
        If trunc is set to True:
            Check the items being printed:
                If they are empty or None -> skip over them
                If they're short (<120 chars) -> print them as normal
                Otherwise -> print a truncated version of them.
        If trunc is set to False:
            Just print everything (all key: value pairs) as is with a little extra spacing.
        """

        return_str = ''

        if trunc:
            for key, val in self.__dict__.items():

                # Just checking (if val) won't work as truth table is ambiguous for length > 1 arrays
                # I know this is gross, but it's the best of a bad situation.
                try:
                    bool(val)
                # Catch numpy array truth table error
                except ValueError:
                    continue

                # Ignore NoneTypes and empty lists / dicts etc unless type is int (charge = 0 for example)
                if val is not None and (val or isinstance(val, int)):
                    return_str += f'\n{key} = '

                    # if it's smaller than 120 chars: print it as is. Otherwise print a version cut off with "...".
                    if len(str(key) + str(val)) < 120:
                        # Print the repr() not the str(). This means generator expressions etc appear too.
                        return_str += repr(val)
                    else:
                        return_str += repr(val)[:121 - len(str(key))] + '...'

        else:
            for key, val in self.__dict__.items():
                # Return all objects as {ligand object name} = {ligand object value(s)} without any special formatting.
                return_str += f'\n{key} = {repr(val)}\n'

        return return_str

    def read_input(self):
        """
        The base input reader used upon class instantiation; it will decide how to handle the input
        based on the file suffix, smiles string or qc_json.
        """

        # Molecule classes are used by qc_json
        if self.mol_input.__class__.__name__ == 'Molecule':
            self.qc_json = self.mol_input
            self.read_qc_json()

        # Check if a file that exists is passed
        elif Path(self.mol_input).exists():
            self.filename = Path(self.mol_input)
            self.name = self.filename.stem
            self.read_file(self.filename, input_type='input')

        # If it's a string, and doesn't contain '.' (not a file that doesn't exist) then it's a smiles string
        elif isinstance(self.mol_input, str) and '.' not in self.mol_input:
            self.smiles = self.mol_input
            self.rdkit_mol = RDKit().smiles_to_rdkit_mol(self.smiles, name=self.name)
            self.mol_from_rdkit(self.rdkit_mol, input_type='input')

        else:
            raise RuntimeError('Cannot parse input. A valid file type, smiles string or qc json must be provided.')

    def read_file(self, input_file, input_type):
        """
        A general file reader that should not be used to instantiate the class.
        Attempts to read file with rdkit, if that fails, QUBEKit file readers are used instead.
        :param input_file: The name of the file to be read
        :param input_type: The type of coordinates it contains ie QM geometry/ MM geometry
        :return: An updated ligand object if the topology matches.
        """

        input_file = Path(input_file)
        try:
            rdkit_mol = RDKit().read_file(input_file)
            self.mol_from_rdkit(rdkit_mol, input_type=input_type)
        except AttributeError:
            if input_type == 'input':
                print('Could not create ligand from RDKit using default readers')
            if input_file.suffix == '.pdb':
                self.read_pdb(input_file, input_type=input_type)
            elif input_file.suffix == '.mol2':
                self.read_mol2(input_file, input_type=input_type)
            elif input_file.suffix == '.xyz':
                self.read_xyz(input_file, input_type=input_type)
            else:
                raise FileTypeError('Unsupported file type.')

    def check_names_are_unique(self):
        """
        To prevent problems occurring with some atoms perceived to be the same,
        check the atom names to ensure they are all unique.
        If some are the same, reset all atom names to be: f'{atomic_symbol}{index}'.
        This ensure they are all unique.
        """

        atom_names = [atom.atom_name for atom in self.atoms]
        # If some atom names aren't unique
        if len(set(atom_names)) < len(atom_names):
            # Change the atom name only; everything else is the same as it was.
            self.atoms = [Atom(atomic_number=atom.atomic_number,
                               atom_index=atom.atom_index,
                               atom_name=f'{atom.atomic_symbol}{i}',
                               partial_charge=atom.partial_charge,
                               formal_charge=atom.formal_charge) for i, atom in enumerate(self.atoms)]

    def mol_from_rdkit(self, rdkit_molecule, input_type='input'):
        """
        Unpack a RDKit molecule into the QUBEKit ligand if instance else just load a valid set of coordinates
        :param rdkit_molecule: The rdkit molecule instance
        :param input_type: Where the coordinates should be stored
        :return: The ligand object with the internal structures if instance
        """

        topology = nx.Graph()
        atoms = []

        if self.name is None:
            self.name = rdkit_molecule.GetProp('_Name')
        # Collect the atom names and bonds
        for atom in rdkit_molecule.GetAtoms():
            # Collect info about each atom
            atomic_number = atom.GetAtomicNum()
            index = atom.GetIdx()
            try:
                # PDB file extraction
                atom_name = atom.GetMonomerInfo().GetName().strip()
            except AttributeError:
                try:
                    # Mol2 file extraction
                    atom_name = atom.GetProp('_TriposAtomName')
                except KeyError:
                    # smiles and mol files have no atom names so generate them here if they are not declared
                    atom_name = f'{atom.GetSymbol()}{index}'

            qube_atom = Atom(atomic_number, index, atom_name, formal_charge=atom.GetFormalCharge())

            # Instance the basic qube_atom
            qube_atom.atom_type = atom.GetSmarts()

            # Add the atoms as nodes
            topology.add_node(atom.GetIdx())

            # Add the bonds
            for bonded in atom.GetNeighbors():
                topology.add_edge(atom.GetIdx(), bonded.GetIdx())
                qube_atom.add_bond(bonded.GetIdx())

            # Now add the atom to the molecule
            atoms.append(qube_atom)

        # Now get the coordinates
        coords = rdkit_molecule.GetConformer().GetPositions()

        # Now get any descriptors we can find
        descriptors = RDKit().rdkit_descriptors(rdkit_molecule)

        self._validate_info(topology, atoms, coords, input_type, rdkit_molecule, descriptors)

    def _validate_info(self, topology, atoms, coords, input_type, rdkit_molecule=None, descriptors=None):
        """
        Check if the provided information should be stored or not
        :param topology: networkx graph of the topology
        :param atoms: a list of Atom objects
        :param coords: a numpy array of the coords
        :param rdkit_molecule: the rdkit molecule we have extracted the info from
        :param descriptors: a dictionary of the rdkit descriptors
        :return: the updated ligand object
        """

        # Now check we instancing the ligand if we are then store the info
        if input_type == 'input':
            self.topology = topology
            self.atoms = atoms
            self.descriptors = descriptors
            self.coords[input_type] = coords
            self.rdkit_mol = rdkit_molecule
        else:
            # Check if the new topology is the same then store the new coordinates
            if nx.algorithms.is_isomorphic(self.topology, topology):
                self.coords[input_type] = coords
            else:
                raise TopologyMismatch('Topologies are not the same; cannot store coordinates.')

    def read_pdb(self, input_file, input_type='input'):
        """
        Reads the input PDB file to find the ATOM or HETATM tags, extracts the elements and xyz coordinates.
        Then reads through the connection tags and builds a connectivity network
        (only works if connections are present in PDB file).
        Bonds are easily found through the edges of the network.
        """

        molecule = []
        topology = nx.Graph()
        atoms = []

        atom_count = 0

        with open(input_file, 'r') as pdb:

            for line in pdb:
                if 'ATOM' in line or 'HETATM' in line:
                    # start collecting the atom class info
                    atomic_symbol = str(line[76:78])
                    atomic_symbol = re.sub('[0-9]+', '', atomic_symbol)
                    atomic_symbol = atomic_symbol.strip()
                    atom_name = str(line.split()[2])

                    # If the element column is missing from the pdb, extract the atomic_symbol from the atom name.
                    if not atomic_symbol:
                        atomic_symbol = str(line.split()[2])[:-1]
                        atomic_symbol = re.sub('[0-9]+', '', atomic_symbol)

                    atomic_number = Element().number(atomic_symbol)
                    # Now instance the qube atom
                    qube_atom = Atom(atomic_number, atom_count, atom_name)
                    atoms.append(qube_atom)

                    # Also add the atom number as the node in the graph
                    topology.add_node(atom_count)
                    atom_count += 1
                    molecule.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])

                if 'CONECT' in line:
                    atom_index = int(line.split()[1]) - 1
                    # Search the connectivity section and add all edges to the graph corresponding to the bonds.
                    for i in range(2, len(line.split())):
                        if int(line.split()[i]) != 0:
                            bonded_index = int(line.split()[i]) - 1
                            topology.add_edge(atom_index, bonded_index)
                            atoms[atom_index].add_bond(bonded_index)
                            atoms[bonded_index].add_bond(atom_index)

        # put the object back into the correct place
        coords = np.array(molecule)
        self._validate_info(topology, atoms, coords, input_type)

    def read_mol2(self, input_file, input_type='input'):
        """
        Read an input mol2 file and extract the atom names, positions, atom types and bonds.
        :param input_file:
        :param input_type: Assign the structure to right holder, input, mm, qm, temp or traj.
        :return: The object back into the right place.
        """

        molecule = []
        topology = nx.Graph()
        atoms = []

        atom_count = 0

        with open(input_file, 'r') as mol2:

            atom_flag = False
            bond_flag = False

            for line in mol2:
                if '@<TRIPOS>ATOM' in line:
                    atom_flag = True
                    continue
                elif '@<TRIPOS>BOND' in line:
                    atom_flag = False
                    bond_flag = True
                    continue
                elif '@<TRIPOS>SUBSTRUCTURE' in line:
                    bond_flag = False
                    continue

                if atom_flag:
                    # Add the molecule information
                    atomic_symbol = line.split()[1][:2]
                    atomic_symbol = re.sub('[0-9]+', '', atomic_symbol)
                    atomic_symbol = atomic_symbol.strip().title()

                    atomic_number = Element().number(atomic_symbol)

                    molecule.append([float(line.split()[2]), float(line.split()[3]), float(line.split()[4])])

                    # Collect the atom names
                    atom_name = str(line.split()[1])

                    # Add the nodes to the topology object
                    topology.add_node(atom_count)
                    atom_count += 1

                    # Get the atom types
                    atom_type = line.split()[5]
                    atom_type = atom_type.replace(".", "")

                    # Make the qube_atom
                    qube_atom = Atom(atomic_number, atom_count, atom_name)
                    qube_atom.atom_type = atom_type

                    atoms.append(qube_atom)

                if bond_flag:
                    # Add edges to the topology network
                    atom_index, bonded_index = int(line.split()[1]) - 1, int(line.split()[2]) - 1
                    topology.add_edge(atom_index, bonded_index)
                    atoms[atom_index].add_bond(bonded_index)
                    atoms[bonded_index].add_bond(atom_index)

        # put the object back into the correct place
        coords = np.array(molecule)
        self._validate_info(topology, atoms, coords, input_type)

    def read_xyz(self, name, input_type='traj'):
        """
        Read an xyz file and get all frames from the file and put in the traj molecule holder by default
        or if there is only one frame change the input location.
        """

        traj_molecules = []
        molecule = []
        try:
            with open(name, 'r') as xyz_file:
                # get the number of atoms
                n_atoms = len(self.atoms)
                for line in xyz_file:
                    line = line.split()
                    # skip frame heading lines
                    if len(line) <= 1:
                        next(xyz_file)
                        continue
                    molecule.append([float(line[1]), float(line[2]), float(line[3])])

                    if len(molecule) == n_atoms:
                        # we have collected the molecule now store the frame
                        traj_molecules.append(np.array(molecule))
                        molecule = []

            # check how many frames we have
            if len(traj_molecules) == 1:
                self.coords[input_type] = traj_molecules[0]
            else:
                self.coords[input_type] = traj_molecules

        except FileNotFoundError:
            raise FileNotFoundError('Cannot find xyz file to read.')

    def read_qc_json(self):
        """
        Using the QC json, extract the atoms and bonds (connectivity) to build a full topology.
        Insert the coords into the molecule too.
        """
        self.topology = nx.Graph()
        self.atoms = []

        for i, atom in enumerate(self.qc_json.symbols):
            self.atoms.append(Atom(atomic_number=Element().number(atom), atom_index=i, atom_name=f'{atom}{i}'))
            self.topology.add_node(i)

        for bond in self.qc_json.connectivity:
            self.topology.add_edge(*bond[:2])

        self.coords['input'] = np.array(self.qc_json.geometry).reshape((len(self.atoms), 3)) * constants.BOHR_TO_ANGS

    def get_atom_with_name(self, name):
        """
        Search through the molecule for an atom with that name and return it when found
        :param name: The name of the atom we are looking for
        :return: The QUBE Atom object with the name
        """

        for atom in self.atoms:
            if atom.atom_name == name:
                return atom
        raise AttributeError('No atom found with that name.')

    def read_geometric_traj(self, trajectory):
        """
        Read in the molecule coordinates to the traj holder from a geometric optimisation using qcengine.
        :param trajectory: The qcengine trajectory
        """

        for frame in trajectory:
            opt_traj = []
            # Convert coordinates from bohr to angstroms
            geometry = np.array(frame['molecule']['geometry']) * constants.BOHR_TO_ANGS
            for i, atom in enumerate(frame['molecule']['symbols']):
                opt_traj.append([geometry[0 + i * 3], geometry[1 + i * 3], geometry[2 + i * 3]])
            self.coords['traj'].append(np.array(opt_traj))

    def find_impropers(self):
        """
        Take the topology graph and find all of the improper torsions in the molecule;
        these are atoms with 3 bonds.
        """

        improper_torsions = []

        for node in self.topology.nodes:
            near = sorted(list(nx.neighbors(self.topology, node)))
            # if the atom has 3 bonds it could be an improper
            # Check if an sp2 carbon or N
            if len(near) == 3 and (self.atoms[node].atomic_symbol == 'C' or self.atoms[node].atomic_symbol == 'N'):
                # Store each combination of the improper torsion
                improper_torsions.append((node, near[0], near[1], near[2]))

        self.improper_torsions = improper_torsions or None

    def find_angles(self):
        """
        Take the topology graph network and return a list of all angle combinations.
        Checked against OPLS-AA on molecules containing 10-63 angles.
        """

        angles = []

        for node in self.topology.nodes:
            bonded = sorted(list(nx.neighbors(self.topology, node)))

            # Check that the atom has more than one bond
            if len(bonded) < 2:
                continue

            # Find all possible angle combinations from the list
            for i in range(len(bonded)):
                for j in range(i + 1, len(bonded), 1):
                    atom1, atom3 = bonded[i], bonded[j]

                    angles.append((atom1, node, atom3))

        self.angles = angles or None

    def find_bond_lengths(self, input_type='input'):
        """For the given molecule and topology find the length of all of the bonds."""

        bond_lengths = {}

        molecule = self.coords[input_type]

        for edge in self.topology.edges:
            atom1 = molecule[edge[0]]
            atom2 = molecule[edge[1]]
            bond_lengths[edge] = np.linalg.norm(atom2 - atom1)

        # Check if the dictionary is full then store else leave as None
        self.bond_lengths = bond_lengths or None

    def find_dihedrals(self):
        """
        Take the topology graph network and again return a dictionary of all possible dihedral combinations
        stored under the central bond keys, which describe the angle.
        """

        dihedrals = {}

        # Work through the network using each edge as a central dihedral bond
        for edge in self.topology.edges:

            for start in list(nx.neighbors(self.topology, edge[0])):

                # Check atom not in main bond
                if start != edge[0] and start != edge[1]:

                    for end in list(nx.neighbors(self.topology, edge[1])):

                        # Check atom not in main bond
                        if end != edge[0] and end != edge[1]:

                            if edge not in dihedrals:
                                # Add the central edge as a key the first time it is used
                                dihedrals[edge] = [(start, edge[0], edge[1], end)]

                            else:
                                # Add the tuple to the correct key.
                                dihedrals[edge].append((start, edge[0], edge[1], end))

        self.dihedrals = dihedrals or None

    def find_rotatable_dihedrals(self):
        """
        For each dihedral in the topology graph network and dihedrals dictionary, work out if the torsion is
        rotatable. Returns a list of dihedral dictionary keys representing the rotatable dihedrals.
        Also exclude standard rotations such as amides and methyl groups.
        """

        if self.dihedrals:
            rotatable = []

            # For each dihedral key remove the edge from the network
            for key in self.dihedrals:
                self.topology.remove_edge(*key)

                # Check if there is still a path between the two atoms in the edges.
                if not nx.has_path(self.topology, *key):
                    rotatable.append(key)

                # Add edge back to the network and try next key
                self.topology.add_edge(*key)

            self.rotatable = rotatable or None

    def get_dihedral_values(self, input_type='input'):
        """
        Taking the molecules' xyz coordinates and dihedrals dictionary, return a dictionary of dihedral
        angle keys and values. Also an option to only supply the keys of the dihedrals you want to calculate.
        """

        if self.dihedrals:

            dih_phis = {}

            molecule = self.coords[input_type]

            for val in self.dihedrals.values():
                for torsion in val:
                    # Calculate the dihedral angle in the molecule using the molecule data array.
                    x1, x2, x3, x4 = [molecule[torsion[i]] for i in range(4)]
                    b1, b2, b3 = x2 - x1, x3 - x2, x4 - x3
                    t1 = np.linalg.norm(b2) * np.dot(b1, np.cross(b2, b3))
                    t2 = np.dot(np.cross(b1, b2), np.cross(b2, b3))
                    dih_phis[torsion] = np.degrees(np.arctan2(t1, t2))

            self.dih_phis = dih_phis or None

    def get_angle_values(self, input_type='input'):
        """
        For the given molecule and list of angle terms measure the angle values,
        then return a dictionary of angles and values.
        """

        angle_values = {}

        molecule = self.coords[input_type]

        for angle in self.angles:
            x1 = molecule[angle[0]]
            x2 = molecule[angle[1]]
            x3 = molecule[angle[2]]
            b1, b2 = x1 - x2, x3 - x2
            cosine_angle = np.dot(b1, b2) / (np.linalg.norm(b1) * np.linalg.norm(b2))
            angle_values[angle] = np.degrees(np.arccos(cosine_angle))

        self.angle_values = angle_values or None

    def symmetrise_bonded_parameters(self):
        """
        Apply symmetry to the parameters stored in the molecule based on types from rdkit.
        """

        if self.bond_types is not None:

            # Collect all of the bond values from the HarmonicBondForce dict
            for bonds in self.bond_types.values():
                bond_lens, bond_forces = zip(*[self.HarmonicBondForce[bond] for bond in bonds])

                # Average
                bond_lens, bond_forces = sum(bond_lens) / len(bond_lens), sum(bond_forces) / len(bond_forces)

                # Replace with averaged values
                for bond in bonds:
                    self.HarmonicBondForce[bond] = [bond_lens, bond_forces]

            # Collect all of the angle values from the HarmonicAngleForce dict
            for angles in self.angle_types.values():
                angle_vals, angle_forces = zip(*[self.HarmonicAngleForce[angle] for angle in angles])

                # Average
                angle_vals, angle_forces = sum(angle_vals) / len(angle_vals), sum(angle_forces) / len(angle_forces)

                # Replace with averaged values
                for angle in angles:
                    self.HarmonicAngleForce[angle] = [angle_vals, angle_forces]

    def write_parameters(self, name=None, is_protein=False):
        """Take the molecule's parameter set and write an xml file for the molecule."""

        # First build the xml tree
        self.build_tree(protein=is_protein)

        tree = self.xml_tree.getroot()
        messy = ET.tostring(tree, 'utf-8')

        pretty_xml_as_string = parseString(messy).toprettyxml(indent="")

        with open(f'{name if name is not None else self.name}.xml', 'w+') as xml_doc:
            xml_doc.write(pretty_xml_as_string)

    def build_tree(self, protein):
        """Separates the parameters and builds an xml tree ready to be used."""

        # Create XML layout
        root = ET.Element('ForceField')
        AtomTypes = ET.SubElement(root, "AtomTypes")
        Residues = ET.SubElement(root, "Residues")

        Residue = ET.SubElement(Residues, "Residue", name=f'{"QUP" if protein else "UNK"}')

        HarmonicBondForce = ET.SubElement(root, "HarmonicBondForce")
        HarmonicAngleForce = ET.SubElement(root, "HarmonicAngleForce")
        PeriodicTorsionForce = ET.SubElement(root, "PeriodicTorsionForce")

        # Assign the combination rule
        c14 = '0.83333' if self.combination == 'amber' else '0.5'
        l14 = '0.5'

        # add the combination rule to the xml for geometric.
        NonbondedForce = ET.SubElement(root, "NonbondedForce", attrib={
            'coulomb14scale': c14, 'lj14scale': l14,
            'combination': self.combination})

        for key, val in self.AtomTypes.items():
            ET.SubElement(AtomTypes, "Type", attrib={
                'name': val[1], 'class': val[2],
                'element': self.atoms[key].atomic_symbol,
                'mass': str(self.atoms[key].atomic_mass)})

            ET.SubElement(Residue, "Atom", attrib={'name': val[0], 'type': val[1]})

        # Add the bonds / connections
        for key, val in self.HarmonicBondForce.items():
            ET.SubElement(Residue, "Bond", attrib={'from': str(key[0]), 'to': str(key[1])})

            ET.SubElement(HarmonicBondForce, "Bond", attrib={
                'class1': self.AtomTypes[key[0]][2],
                'class2': self.AtomTypes[key[1]][2],
                'length': f'{val[0]:.6f}', 'k': f'{val[1]:.6f}'})

        # Add the angles
        for key, val in self.HarmonicAngleForce.items():
            ET.SubElement(HarmonicAngleForce, "Angle", attrib={
                'class1': self.AtomTypes[key[0]][2],
                'class2': self.AtomTypes[key[1]][2],
                'class3': self.AtomTypes[key[2]][2],
                'angle': f'{val[0]:.6f}', 'k': f'{val[1]:.6f}'})

        # add the proper and improper torsion terms
        for key in self.PeriodicTorsionForce:
            if self.PeriodicTorsionForce[key][-1] == 'Improper':
                tor_type = 'Improper'
            else:
                tor_type = 'Proper'
            ET.SubElement(PeriodicTorsionForce, tor_type, attrib={
                'class1': self.AtomTypes[key[0]][2],
                'class2': self.AtomTypes[key[1]][2],
                'class3': self.AtomTypes[key[2]][2],
                'class4': self.AtomTypes[key[3]][2],
                'k1': str(self.PeriodicTorsionForce[key][0][1]),
                'k2': str(self.PeriodicTorsionForce[key][1][1]),
                'k3': str(self.PeriodicTorsionForce[key][2][1]),
                'k4': str(self.PeriodicTorsionForce[key][3][1]),
                'periodicity1': '1', 'periodicity2': '2',
                'periodicity3': '3', 'periodicity4': '4',
                'phase1': str(self.PeriodicTorsionForce[key][0][2]),
                'phase2': str(self.PeriodicTorsionForce[key][1][2]),
                'phase3': str(self.PeriodicTorsionForce[key][2][2]),
                'phase4': str(self.PeriodicTorsionForce[key][3][2])})

        # add the non-bonded parameters
        for key in self.NonbondedForce:
            ET.SubElement(NonbondedForce, "Atom", attrib={
                'type': self.AtomTypes[key][1],
                'charge': f'{self.NonbondedForce[key][0]:.6f}',
                'sigma': f'{self.NonbondedForce[key][1]:.6f}',
                'epsilon': f'{self.NonbondedForce[key][2]:.6f}'})

        # Add all of the virtual site info if present
        if self.sites:
            # Add the atom type to the top
            for key, val in self.sites.items():
                ET.SubElement(AtomTypes, "Type", attrib={
                    'name': f'v-site{key + 1}', 'class': f'X{key + 1}', 'mass': '0'})

                # Add the atom info
                ET.SubElement(Residue, "Atom", attrib={
                    'name': f'X{key + 1}', 'type': f'v-site{key + 1}'})

                # Add the local coords site info
                ET.SubElement(Residue, "VirtualSite", attrib={
                    'type': 'localCoords',
                    'index': str(key + len(self.atoms)),
                    'atom1': str(val[0][0]), 'atom2': str(val[0][1]), 'atom3': str(val[0][2]),
                    'wo1': '1.0', 'wo2': '0.0', 'wo3': '0.0',
                    'wx1': '-1.0', 'wx2': '1.0', 'wx3': '0.0',
                    'wy1': '-1.0', 'wy2': '0.0', 'wy3': '1.0',
                    'p1': f'{float(val[1][0]):.4f}',
                    'p2': f'{float(val[1][1]):.4f}',
                    'p3': f'{float(val[1][2]):.4f}'})

                # Add the nonbonded info
                ET.SubElement(NonbondedForce, "Atom", attrib={
                    'type': f'v-site{key + 1}',
                    'charge': f'{val[2]}',
                    'sigma': '1.000000',
                    'epsilon': '0.000000'})

        # Store the tree back into the molecule
        self.xml_tree = ET.ElementTree(root)

    def write_xyz(self, input_type='input', name=None):
        """
        Write a general xyz file of the molecule if there are multiple geometries in the molecule write a traj
        :param input_type: Where the molecule coordinates are taken from
        :param name: The name of the xyz file to be produced; otherwise self.name is used.
        """

        with open(f'{name if name is not None else self.name}.xyz', 'w+') as xyz_file:

            if len(self.coords[input_type]) / len(self.atoms) == 1:
                message = 'xyz file generated with QUBEKit'
                end = ''
                trajectory = [self.coords[input_type]]

            else:
                message = f'QUBEKit xyz trajectory FRAME '
                end = 1
                trajectory = self.coords[input_type]

            # Write out each frame
            for frame in trajectory:

                xyz_file.write(f'{len(self.atoms)}\n')
                xyz_file.write(f'{message}{end}\n')

                for i, atom in enumerate(frame):
                    xyz_file.write(
                        f'{self.atoms[i].atomic_symbol}       {atom[0]: .10f}   {atom[1]: .10f}   {atom[2]: .10f}\n')

                try:
                    end += 1
                except TypeError:
                    # This is the result of only printing one frame so catch the error and ignore
                    pass

    def write_gromacs_file(self, input_type='input'):
        """To a gromacs file, write and format the necessary variables gro."""

        with open(f'{self.name}.gro', 'w+') as gro_file:
            gro_file.write(f'NEW {self.name.upper()} GRO FILE\n')
            gro_file.write(f'{len(self.coords[input_type]):>5}\n')
            for pos, atom in enumerate(self.coords[input_type], 1):
                # 'mol number''mol name'  'atom name'   'atom count'   'x coord'   'y coord'   'z coord'
                # 1WATER  OW1    1   0.126   1.624   1.679
                gro_file.write(
                    f'    1{self.name.upper()}  {atom[0]}{pos}   {pos}   '
                    f'{atom[1]: .3f}   {atom[2]: .3f}   {atom[3]: .3f}\n')

    def pickle(self, state=None):
        """
        Pickles the Molecule object in its current state to the (hidden) pickle file.
        If other pickle objects already exist for the particular object:
            the latest object is put to the top.
        """

        mols = OrderedDict()
        # First check if the pickle file exists
        try:
            # Try to load a hidden pickle file; make sure to get all objects
            with open('.QUBEKit_states', 'rb') as pickle_jar:
                while True:
                    try:
                        mol = pickle.load(pickle_jar)
                        mols[mol.state] = mol
                    except EOFError:
                        break
        except FileNotFoundError:
            pass

        # Now we can save the items; first assign the location
        self.state = state
        mols[self.state] = self

        # Open the pickle jar which will always be the ligand object's name
        with open(f'.QUBEKit_states', 'wb') as pickle_jar:

            # If there were other molecules of the same state in the jar: overwrite them
            for val in mols.values():
                pickle.dump(val, pickle_jar)

    def get_bond_equiv_classes(self):
        """
        Using the symmetry dict, give each bond a code. If any codes match, the bonds can be symmetrised.
        e.g. bond_symmetry_classes = {(0, 3): '2-0', (0, 4): '2-0', (0, 5): '2-0' ...}
        all of the above bonds (tuples) are of the same type (methyl H-C bonds in same region)
        This dict is then used to produce bond_types.
        bond_types is just a dict where the keys are the string code from above and the values are all
        of the bonds with that particular type.
        """

        bond_symmetry_classes = {}
        for bond in self.topology.edges:
            bond_symmetry_classes[bond] = (f'{self.atom_symmetry_classes[bond[0]]}-'
                                           f'{self.atom_symmetry_classes[bond[1]]}')

        bond_types = {}
        for key, val in bond_symmetry_classes.items():
            bond_types.setdefault(val, []).append(key)

        self.bond_types = self._cluster_types(bond_types)

    def get_angle_equiv_classes(self):
        """
        Using the symmetry dict, give each angle a code. If any codes match, the angles can be symmetrised.
        e.g. angle_symmetry_classes = {(1, 0, 3): '3-2-0', (1, 0, 4): '3-2-0', (1, 0, 5): '3-2-0' ...}
        all of the above angles (tuples) are of the same type (methyl H-C-H angles in same region)
        angle_types is just a dict where the keys are the string code from the above and the values are all
        of the angles with that particular type.
        """

        angle_symmetry_classes = {}
        for angle in self.angles:
            angle_symmetry_classes[angle] = (f'{self.atom_symmetry_classes[angle[0]]}-'
                                             f'{self.atom_symmetry_classes[angle[1]]}-'
                                             f'{self.atom_symmetry_classes[angle[2]]}')

        angle_types = {}
        for key, val in angle_symmetry_classes.items():
            angle_types.setdefault(val, []).append(key)

        self.angle_types = self._cluster_types(angle_types)

    def get_dihedral_equiv_classes(self):
        """
        Using the symmetry dict, give each dihedral a code. If any codes match, the dihedrals can be clustered and their
        parameters should be the same, this is to be used in dihedral fitting so all symmetry equivalent dihedrals are
        optimised at the same time. dihedral_equiv_classes = {(0, 1, 2 ,3): '1-1-2-1'...} all of the tuples are the
        dihedrals index by topology and the strings are the symmetry equivalent atom combinations.
        """

        dihedral_symmetry_classes = {}
        for dihedral_set in self.dihedrals.values():
            for dihedral in dihedral_set:
                dihedral_symmetry_classes[tuple(dihedral)] = (f'{self.atom_symmetry_classes[dihedral[0]]}-'
                                                              f'{self.atom_symmetry_classes[dihedral[1]]}-'
                                                              f'{self.atom_symmetry_classes[dihedral[2]]}-'
                                                              f'{self.atom_symmetry_classes[dihedral[3]]}')

        dihedral_types = {}
        for key, val in dihedral_symmetry_classes.items():
            dihedral_types.setdefault(val, []).append(key)

        self.dihedral_types = self._cluster_types(dihedral_types)

    def _cluster_types(self, equiv_classes):
        """
        Function that helps the bond angle and dihedral class finders in clustering the types based on the forward and
        backward type strings.
        :return: clustered equiv class
        """

        new_classes = {}
        for key, item in equiv_classes.items():
            try:
                new_classes[key].extend(item)
            except KeyError:
                try:
                    new_classes[key[::-1]].extend(item)
                except KeyError:
                    new_classes[key] = item

        return new_classes

    def symmetrise_from_topo(self):
        """
        First, if rdkit_mol has been generated, get the bond and angle symmetry dicts.
        These will be used by L-J and the Harmonic Bond/Angle params

        Then, based on the molecule topology, symmetrise the methyl / amine hydrogens.
        If there's a carbon, does it have 3/2 hydrogens? -> symmetrise
        If there's a nitrogen, does it have 2 hydrogens? -> symmetrise
        Also keep a list of the methyl carbons and amine / nitrile nitrogens
        then exclude these bonds from the rotatable torsions list.
        """
        if self.rdkit_mol is not None:

            self.atom_symmetry_classes = RDKit().find_symmetry_classes(self.rdkit_mol)

            self.get_bond_equiv_classes()
            self.get_angle_equiv_classes()

            if self.dihedrals:
                self.get_dihedral_equiv_classes()

        methyl_hs, amine_hs, other_hs = [], [], []
        methyl_amine_nitride_cores = []

        for atom in self.atoms:
            if atom.atomic_symbol == 'C' or atom.atomic_symbol == 'N':

                hs = []
                for bonded in self.topology.neighbors(atom.atom_index):
                    if len(list(self.topology.neighbors(bonded))) == 1:
                        # now make sure it is a hydrogen (as halogens could be caught here)
                        if self.atoms[bonded].atomic_symbol == 'H':
                            hs.append(bonded)

                if atom.atomic_symbol == 'C' and len(hs) == 2:    # This is part of a carbon hydrogen chain
                    other_hs.append(hs)
                elif atom.atomic_symbol == 'C' and len(hs) == 3:
                    methyl_hs.append(hs)
                    methyl_amine_nitride_cores.append(atom.atom_index)
                elif atom.atomic_symbol == 'N' and len(hs) == 2:
                    amine_hs.append(hs)
                    methyl_amine_nitride_cores.append(atom.atom_index)
                elif atom.atomic_symbol == 'N' and len(hs) == 1:
                    methyl_amine_nitride_cores.append(atom.atom_index)

        self.symm_hs = {'methyl': methyl_hs, 'amine': amine_hs, 'other': other_hs}

        # now modify the rotatable list to remove methyl and amine / nitrile torsions
        # these are already well represented in most FF's
        remove_list = []
        if self.rotatable is not None:
            rotatable = self.rotatable
            for key in rotatable:
                if key[0] in methyl_amine_nitride_cores or key[1] in methyl_amine_nitride_cores:
                    remove_list.append(key)

            # now remove the keys
            for torsion in remove_list:
                rotatable.remove(torsion)

            self.rotatable = rotatable or None

    def openmm_coordinates(self, input_type='input'):
        """
        Take a set of coordinates from the molecule and convert them to OpenMM format
        :param input_type: The set of coordinates that should be used
        :return: A list of tuples of the coords
        """

        coordinates = self.coords[input_type]

        if input_type == 'traj' and len(coordinates) != len(self.coords['input']):
            # Multiple frames in this case
            return [[tuple(atom / 10) for atom in frame] for frame in coordinates]
        else:
            return [tuple(atom / 10) for atom in coordinates]

    def read_tdrive(self, bond_scan):
        """
        Read a tdrive qdata file and get the coordinates and scan energies and store in the molecule.
        :type bond_scan: the tuple of the scanned central bond
        :return: None, store the coords in the traj holder and the energies in the qm scan holder
        """

        scan_coords = []
        energy = []
        qm_scans = {}
        with open('qdata.txt', 'r') as data:
            for line in data.readlines():
                if 'COORDS' in line:
                    coords = [float(x) for x in line.split()[1:]]
                    coords = np.array(coords).reshape((len(self.atoms), 3))
                    scan_coords.append(coords)
                elif 'ENERGY' in line:
                    energy.append(float(line.split()[1]))

        qm_scans[bond_scan] = [np.array(energy), scan_coords]
        if self.qm_scans is not None:
            self.qm_scans = {**self.qm_scans, **qm_scans}
        else:
            self.qm_scans = qm_scans or None

    def read_scan_order(self, file):
        """
        Read a qubekit or tdrive dihedrals file and store the scan order into the ligand class
        :param file: The dihedrals input file.
        :return: The molecule with the scan_order saved
        """

        # If we have a QUBE.dihedrals file get the scan order from there
        scan_order = []
        torsions = open(file).readlines()
        for line in torsions[2:]:
            torsion = line.split()
            if len(torsion) == 4:
                core = (int(torsion[1]), int(torsion[2]))
                if core in self.dihedrals.keys():
                    scan_order.append(core)
                elif reversed(tuple(core)) in self.dihedrals.keys():
                    scan_order.append(reversed(tuple(core)))

        self.scan_order = scan_order


class Ligand(DefaultsMixin, Molecule):

    def __init__(self, mol_input, name=None):
        """
        parameter_engine        A string keeping track of the parameter engine used to assign the initial parameters
        hessian                 2d numpy array; matrix of size 3N x 3N where N is number of atoms in the molecule
        modes                   A list of the qm predicted frequency modes
        home

        constraints_file        Either an empty string (does nothing in geometric run command); or
                                the abspath of the constraint.txt file (constrains the execution of geometric)
        """

        super().__init__(mol_input, name)

        self.parameter_engine = 'openmm'
        self.hessian = None
        self.modes = None
        self.home = None

        self.constraints_file = None

        # Make sure we have the topology before we calculate the properties
        if self.topology.edges:
            self.find_angles()
            self.find_dihedrals()
            self.find_rotatable_dihedrals()
            self.find_impropers()
            self.get_dihedral_values()
            self.find_bond_lengths()
            self.get_angle_values()
            self.symmetrise_from_topo()

    def write_pdb(self, input_type='input', name=None):
        """
        Take the current molecule and topology and write a pdb file for the molecule.
        Only for small molecules, not standard residues. No size limit.
        """

        molecule = self.coords[input_type]

        with open(f'{name if name is not None else self.name}.pdb', 'w+') as pdb_file:

            # Write out the atomic xyz coordinates
            pdb_file.write(f'REMARK   1 CREATED WITH QUBEKit {datetime.now()}\n')
            pdb_file.write(f'COMPND    {self.name:<20}\n')
            for i, atom in enumerate(molecule):
                pdb_file.write(
                    f'HETATM {i+1:>4}{self.atoms[i].atom_name:>4}  UNL     1{atom[0]:12.3f}{atom[1]:8.3f}{atom[2]:8.3f}'
                    f'  1.00  0.00         {self.atoms[i].atomic_symbol.title():>3}\n')

            # Now add the connection terms
            for node in self.topology.nodes:
                bonded = sorted(list(nx.neighbors(self.topology, node)))
                if len(bonded) > 1:
                    pdb_file.write(f'CONECT{node + 1:5}{"".join(f"{x + 1:5}" for x in bonded)}\n')

            pdb_file.write('END\n')


class Protein(DefaultsMixin, Molecule):
    """This class handles the protein input to make the qubekit xml files and rewrite the pdb so we can use it."""

    def __init__(self, filename):

        super().__init__(filename)

        self.pdb_names = None
        # TODO Needs updating with new Path method of handling filenames
        self.read_pdb(self.filename)
        self.residues = None
        self.home = os.getcwd()

    def read_pdb(self, input_file, input_type='input'):
        """
        Read the pdb file which probably does not have the right connections,
        so we need to find them using QUBE.xml
        """

        with open(input_file, 'r') as pdb:
            lines = pdb.readlines()

        protein = []
        self.topology = nx.Graph()
        self.residues = []
        self.Residues = []
        self.pdb_names = []
        self.atoms = []

        # atom counter used for graph node generation
        atom_count = 0
        for line in lines:
            if 'ATOM' in line or 'HETATM' in line:
                atomic_symbol = str(line[76:78])
                atomic_symbol = re.sub('[0-9]+', '', atomic_symbol).strip()

                # If the element column is missing from the pdb, extract the atomic_symbol from the atom name.
                if not atomic_symbol:
                    atomic_symbol = str(line.split()[2])
                    atomic_symbol = re.sub('[0-9]+', '', atomic_symbol)

                # now make sure we have a valid element
                if atomic_symbol.lower() != 'cl' and atomic_symbol.lower() != 'br':
                    atomic_symbol = atomic_symbol[0]

                atom_name = f'{atomic_symbol}{atom_count}'
                qube_atom = Atom(Element().number(atomic_symbol), atom_count, atom_name)

                self.atoms.append(qube_atom)

                self.pdb_names.append(str(line.split()[2]))

                # also get the residue order from the pdb file so we can rewrite the file
                self.Residues.append(str(line.split()[3]))

                # Also add the atom number as the node in the graph
                self.topology.add_node(atom_count)
                atom_count += 1
                protein.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])

            elif 'CONECT' in line:
                # Now look through the connectivity section and add all edges to the graph corresponding to the bonds.
                for i in range(2, len(line.split())):
                    if not int(line.split()[i]):
                        self.topology.add_edge(int(line.split()[1]) - 1, int(line.split()[i]) - 1)

        self.coords[input_type] = np.array(protein)

        # check if there are any conect terms in the file first
        # if not self.topology.edges:
        if not len(self.topology.edges):
            print('No connections found!')
        else:
            self.find_angles()
            self.find_dihedrals()
            self.find_rotatable_dihedrals()
            self.find_impropers()
            self.get_dihedral_values()
            self.find_bond_lengths()
            self.get_angle_values()
            self.symmetrise_from_topo()

        # TODO What if there are two or more of the same residue back to back?
        #   Need to store the number of atoms in each amino acid and use that to check instead.
        # Remove duplicates
        self.residues = [res for res, group in groupby(self.Residues)]

    def write_pdb(self, name=None):
        """This method replaces the ligand method as all of the atom names and residue names have to be replaced."""

        molecule = self.coords['input']

        with open(f'{name if name is not None else self.name}.pdb', 'w+') as pdb_file:

            # Write out the atomic xyz coordinates
            pdb_file.write(f'REMARK   1 CREATED WITH QUBEKit {datetime.now()}\n')
            # pdb_file.write(f'COMPND    {self.name:<20}\n')
            # we have to transform the atom name while writing out the pdb file
            for i, atom in enumerate(molecule):
                pdb_file.write(
                    f'HETATM {i+1:>4}{self.atoms[i].atom_name:>4}  QUP     1{atom[0]:12.3f}{atom[1]:8.3f}{atom[2]:8.3f}'
                    f'  1.00  0.00         {self.atoms[i].atomic_symbol.upper():>3}\n')

            # Now add the connection terms
            for node in self.topology.nodes:
                bonded = sorted(list(nx.neighbors(self.topology, node)))
                if len(bonded) >= 1:
                    pdb_file.write(f'CONECT{node + 1:5}{"".join(f"{x + 1:5}" for x in bonded)}\n')

            pdb_file.write('END\n')

    def update(self, input_type='input'):
        """
        After the protein has been passed to the parametrisation class we get back the bond info
        use this to update all missing terms.
        """

        # using the new harmonic bond force dict we can add the bond edges to the topology graph
        for bond in self.HarmonicBondForce:
            self.topology.add_edge(*bond)

        self.find_angles()
        self.find_dihedrals()
        self.find_rotatable_dihedrals()
        self.get_dihedral_values(input_type)
        self.find_bond_lengths(input_type)
        self.get_angle_values(input_type)
        self.find_impropers()
        # this creates the dictionary of terms that should be symmetrise
        self.symmetrise_from_topo()
