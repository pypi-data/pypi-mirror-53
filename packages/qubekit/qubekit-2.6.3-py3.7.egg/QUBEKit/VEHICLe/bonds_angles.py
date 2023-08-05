"""
Get the hessians from the VEHICLe dataset

Get the json dict from qcportal
From this, initialise a Ligand object, add in the qm-optimised coords and hessian
Generate a

"""

from QUBEKit.engines import RDKit
from QUBEKit.ligand import Ligand
from QUBEKit.mod_seminario import ModSeminario
from QUBEKit.parametrisation.base_parametrisation import Parametrisation
from QUBEKit.utils import constants
from QUBEKit.utils.helpers import check_symmetry

import os
from pathlib import Path
import pickle

import numpy as np
import pandas as pd
import qcportal as ptl

from rdkit import DataStructs
from rdkit.Chem import AllChem


class BondsAndAngles:

    def __init__(self):
        self.client, self.ds, self.records = None, None, None
        self.get_records()

        self.bond_data = []
        self.bond_labels = []

        self.angle_data = []
        self.angle_labels = []

    def get_records(self):
        if os.path.exists('records.pkl'):
            with open('records.pkl', 'rb') as rec_file:
                self.client, self.ds, self.records = pickle.load(rec_file)
        else:
            # Cache VEHICLe dataset
            self.client = ptl.FractalClient()
            self.client.list_collections('OptimizationDataset')
            self.ds = self.client.get_collection('OptimizationDataset', 'OpenFF VEHICLe Set 1')
            self.ds.df.head()
            self.ds.list_specifications()

            # Cache records
            self.records = self.ds.data.records
            pickle_data = (self.client, self.ds, self.records)

            with open('records.pkl', 'wb') as rec_file:
                pickle.dump(pickle_data, rec_file)

    def loop_over_mols(self):
        for i, item in enumerate(self.records):
            try:
                ptl_name = item.strip('\n')
                smiles = self.records[ptl_name].attributes['canonical_smiles']
                print(f'iter: {str(i).zfill(5)}; smiles: {smiles}')

                # Specific ID of given smiles string
                try:
                    opt_record = self.ds.get_entry(ptl_name).object_map['default']
                except KeyError:
                    continue

                # Optimisation of molecule at ID: opt_record
                optimisation = self.client.query_procedures(id=opt_record)[0]

                # Extract hessian
                try:
                    # TODO Hessian shape has been changed?
                    hessian = self.client.query_results(molecule=optimisation.final_molecule, driver='hessian')[0].return_result
                except IndexError:
                    # Molecule has been optimised but no hessian has been calculated yet
                    continue

                # Reshape hessian
                conversion = constants.HA_TO_KCAL_P_MOL / (constants.BOHR_TO_ANGS ** 2)
                hessian = np.array(hessian).flatten()
                hessian = hessian.reshape(int(len(hessian) ** 0.5), -1) * conversion

                # check_symmetry(hessian)

                # Extract optimised structure
                opt_struct = self.client.query_procedures(id=opt_record)[0].get_final_molecule()

                mol = self.calc_mod_sem(smiles, hessian, opt_struct)
                finger_prints = self.calc_fingerprint()
                self.format_data(mol, finger_prints)

            # Can Ctrl-C to stop program and it'll still try to store the data up to that point
            except BaseException as exc:
                # Pickle the results every iteration so that an error won't mean progress is lost.
                # dedent if this isn't wanted.
                # self.pickle_results()
                self.bond_data = np.array(self.bond_data)
                np.save('test_data', self.bond_data)
                self.bond_labels = np.array(self.bond_labels)
                np.save('test_labels', self.bond_labels)

                raise exc

    @staticmethod
    def calc_mod_sem(smiles, hessian, opt_struct):

        # Initialise Ligand object using the json dict from qcengine
        mol = Ligand(opt_struct, name='initial_test')

        # Set the qm coords to the input coords from qcengine
        mol.coords['qm'] = mol.coords['input']

        # Insert hessian and optimised coordinates
        mol.hessian = hessian
        mol.parameter_engine = 'none'

        # Create empty parameter dicts
        Parametrisation(mol).gather_parameters()

        # Add some spacing and the smiles to the read-only output file
        with open('Modified_Seminario_Bonds.txt', 'a+') as bonds_file,\
                open('Modified_Seminario_Angles.txt', 'a+') as angles_file:
            bonds_file.write(f'\n\n{smiles}\n\n')
            angles_file.write(f'\n\n{smiles}\n\n')

        # Get Mod Sem angle and bond params
        ModSeminario(mol).modified_seminario_method()

        # Write a pdb to preserve order for RDKit
        mol.write_pdb(name='test')

        return mol

    @staticmethod
    def calc_fingerprint():

        rdkit_mol = RDKit().read_file(Path('test.pdb'))

        finger_prints = {}
        for atom in rdkit_mol.GetAtoms():
            atom_index = atom.GetIdx()
            fp = AllChem.GetHashedAtomPairFingerprintAsBitVect(rdkit_mol, maxLength=4, fromAtoms=[atom_index])
            arr = np.zeros(1, )
            DataStructs.ConvertToNumpyArray(fp, arr)
            finger_prints[atom_index] = arr

        os.system('rm test.pdb')

        return finger_prints

    def format_data(self, mol, finger_prints):

        for bond, val in mol.HarmonicBondForce.items():
            self.bond_data.append(np.concatenate((finger_prints[bond[0]], finger_prints[bond[1]])))
            self.bond_labels.append(val)

    # def pickle_results(self):
    #
    #     with open('bond_train.pkl', 'wb') as bond_data_file, open('bond_label.pkl', 'wb') as bond_label_file:
    #         pickle.dump(self.bond_data, bond_data_file)
    #         pickle.dump(self.bond_labels, bond_label_file)
    #
    #     with open('angle_train.pkl', 'wb') as angle_data_file, open('angle_label.pkl', 'wb') as angle_label_file:
    #         pickle.dump(self.angle_data, angle_data_file)
    #         pickle.dump(self.angle_labels, angle_label_file)


if __name__ == '__main__':
    BondsAndAngles().loop_over_mols()

    # data = np.load('test_data.npy')
    # other = np.load('test_labels.npy')
    # print(data)
    # print(other)
