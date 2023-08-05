# # #!/usr/bin/env python
#
# # from collections import OrderedDict
# # import os
# #
# # import matplotlib.pyplot as plt
# # import matplotlib.lines as mlines
# # from numpy import arange
# # from numpy.polynomial.polynomial import polyfit
# #
# # import networkx as nx
# #
# #
# # def main():
# #     """
# #     Currently you cannot pass marker style as a list in Matplotlib.
# #     To get around that, the data could be grouped by atom type and the colour passed as a list.
# #     Then it would be possible to plot atoms which are the same type together,
# #     while also maintaining the correct colours from the molecule names.
# #
# #     Anyway, this function collects the data from the txt file for ONETEP, DDEC3&6 charges.
# #     The data are stored in a dictionary where the keys are the molecule names
# #     and the values are a list of lists. Each nested list is an atom in the form:
# #     ['Atom Type', 'DDEC3 charge', 'DDEC6 charge', 'ONETEP charge']
# #
# #     Overall, this gives something like:
# #
# #     data = {'Benzene': [['C', '-0.108887', '-0.101384', '-0.1146'], ['C', ... ], ... ], 'Methane': ... }
# #
# #     The data are transformed to floats in the graphing section.
# #     """
# #
# #     font = {'family': 'sans-serif',
# #             # 'weight': 'bold',
# #             'size': 14}
# #
# #     plt.rc('font', **font)
# #
# #     data = dict()
# #
# #     # Extract molecule data, using 'Atom' header as start marker, and 'p' as end marker
# #     with open('../../../Documents/QUBEKit_vs_ONETEP/comparison_data.txt', 'r') as file:
# #         lines = file.readlines()
# #
# #     for count, line in enumerate(lines):
# #         if line.startswith('Atom'):
# #             data[lines[count - 1][:-1]] = []
# #             i = 1
# #             while lines[count + i].split()[0] != 'p':
# #                 data[lines[count - 1][:-1]].append(lines[count + i].split())
# #                 i += 1
# #
# #     # Can change colours used here if you want. Currently just using defaults.
# #     colours = {'Acetamide': 'r', 'Benzene': 'b', 'Acetic acid': 'y',
# #                'Acetophenone': 'k', 'Aniline': 'g', 'DMSO': 'm',
# #                '2-Heptanone': 'c', '1-Octanol': 'grey', 'Phenol': 'indigo',
# #                'Pyridine': 'olive'}
# #
# #     # Marker dict to change element names to Matplotlib marker styles.
# #     markers = {'O': 'o', 'C': '<', 'H': 's', 'N': 'd', 'S': '*'}
# #
# #     # Apply marker changes across all molecules' atoms (massive pain to implement into graph so currently useless).
# #     for key, val in data.items():
# #         for i in range(len(val)):
# #             data[key][i][0] = markers[data[key][i][0]]
# #
# #     # Indicates the column positions for extracting from data = { ... }
# #     mark, ddec3, ddec6, onetep = 0, 1, 2, 3
# #
# #     fig, (ax1, ax2) = plt.subplots(1, 2)
# #
# #     ax1.set_autoscaley_on(False)
# #     ax1.set_xlim([-1, 1])
# #     ax1.set_ylim([-1, 1])
# #     ax1.set(adjustable='box-forced', aspect='equal')
# #
# #     # Add black diagonal line for reference.
# #     line = mlines.Line2D([0, 1], [0, 1], color='k')
# #     transform = ax1.transAxes
# #     line.set_transform(transform)
# #     ax1.add_line(line)
# #
# #     [ax1.scatter([float(col[onetep]) for col in val], [float(col[ddec3]) for col in val],
# #                  marker='x', s=80) for key, val in data.items()]
# #
# #     ax1.set_xlabel('ONETEP')
# #     ax1.set_ylabel('QUBEKit (IPCM, DDEC3)')
# #     ax1.grid(True)
# #     ax1.annotate('R² = 0.984', xy=(-0.8, 0.8))
# #
# #     # Best fit
# #     x = arange(-1, 2)
# #     y = 0.9095 * x - 3 * (10 ** -8)
# #     b, m = polyfit(x, y, 1)
# #     ax1.plot(x, b + m * x, '-')
# #
# #     ax2.set_autoscaley_on(False)
# #     ax2.set_xlim([-1, 1])
# #     ax2.set_ylim([-1, 1])
# #     ax2.set(adjustable='box-forced', aspect='equal')
# #
# #     line = mlines.Line2D([0, 1], [0, 1], color='k')
# #     transform = ax2.transAxes
# #     line.set_transform(transform)
# #     ax2.add_line(line)
# #
# #     [ax2.scatter([float(col[ddec6]) for col in val], [float(col[ddec3]) for col in val],
# #                  marker='x', s=80) for key, val in data.items()]
# #
# #     ax2.set_xlabel('QUBEKit (IPCM, DDEC6)')
# #     ax2.set_ylabel('QUBEKit (IPCM, DDEC3)')
# #     ax2.grid(True)
# #     ax2.annotate('R² = 0.944', xy=(-0.8, 0.8))
# #
# #     # Best fit
# #     x = arange(-1, 2)
# #     y = 1.1255 * x + 0.0021
# #     b, m = polyfit(x, y, 1)
# #     ax2.plot(x, b + m * x, '-')
# #
# #     plt.legend(['Equally Charged', 'LSR'] + [str(key) for key, val in data.items()], loc='lower right')
# #
# #     plt.show()
# #
# #
# # def parse_molecules():
# #
# #     folder_names = []
# #     for root, dirs, files in os.walk('../../../Documents/SI_data/molecules'):
# #         folder_names.append(dirs)
# #
# #     folder_names = [folder for folder in folder_names if folder]
# #     folder_names = folder_names[0]
# #
# #     for folder in folder_names:
# #         try:
# #             os.system(f'cp ../../../Documents/SI_data/molecules/{folder}/MOL.pdb ../../../Documents/test_set/{folder.replace(",", "_").replace("-", "_")}.pdb')
# #             os.system(f'cp ../../../Documents/SI_data/molecules/{folder}/MOL.xml ../../../Documents/test_set/{folder.replace(",", "_").replace("-", "_")}.xml')
# #         except:
# #             pass
# #
#
# # import matplotlib.animation as animation
# #
# #
# # fig = plt.figure()
# # ax1 = fig.add_subplot(1, 1, 1)
# #
# #
# # def animate(i):
# #
# #     pull_data = open('sample_data.txt').read()
# #     data_array = pull_data.split('\n')
# #     xar = []
# #     yar = []
# #     for each_line in data_array:
# #         if len(each_line) > 1:
# #             x, y = each_line.split(',')
# #             xar.append(int(x))
# #             yar.append(int(y))
# #     ax1.clear()
# #     ax1.plot(xar, yar)
# #
# #
# # ani = animation.FuncAnimation(fig, animate, interval=1000)
# #
# # plt.show()
#
#
# # class Person:
# #
# #     def __init__(self, firstname, lastname):
# #
# #         self.first = firstname
# #         self.last = lastname
# #         self.fullname = self.fullname()
# #         self.email = self.email()
# #
# #     def fullname(self):
# #         return f'{self.first} {self.last}'
# #
# #     def email(self):
# #         return f'{self.first}.{self.last}@email.com'
# #
# #
# # pers = Person('Chris', 'Ringrose')
# #
# # # print(pers.email)
# #
# #
# # class Person2:
# #
# #     def __init__(self, firstname, lastname):
# #
# #         self.first = firstname
# #         self.last = lastname
# #
# #     @property
# #     def fullname(self):
# #         return f'{self.first} {self.last}'
# #
# #     @fullname.setter
# #     def fullname(self, name):
# #         self.first, self.last = name.split()
# #
# #     @property
# #     def email(self):
# #         return f'{self.first}.{self.last}@email.com'
# #
# #     @email.setter
# #     def email(self, email):
# #         name = email[:-10].replace('.', ' ')
# #         self.first, self.last = name.split()
# #
# #
# # pers2 = Person2('chris', 'ringrose')
# #
# # print(pers2.fullname)
# #
# # pers2.email = 'josh.horton@email.com'
# # # per.fullname = 'josh horton'
# #
# # print(pers2.fullname)
#
#
# import csv
#
#
# # with open('liquid_props.csv') as old_csv, open('liq_props.csv', 'w') as new_csv:
# #
# #     reader = csv.reader(old_csv, delimiter=',')
# #     writer = csv.writer(new_csv, delimiter=',')
# #     for row in reader:
# #         writer.writerow([row[0].replace(",", "_").replace("-", "_")] + row[1:])
#
#
# def parse_molecules():
#
#     with open('final.csv', 'w') as final:
#         file_writer = csv.writer(final, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#         file_writer.writerow(['name', 'smiles',
#                               'exp_vap', 'old_vap', 'old_vap_err', 'new_vap', 'new_vap_err',
#                               'exp_dens', 'old_dens', 'old_dens_err', 'new_dens', 'new_dens_err'])
#
#     with open('liq_props.csv') as old_csv, open('results.csv') as results, open('results_old.csv') as results_old:
#
#         old_reader = csv.reader(old_csv, delimiter=',')
#         # new_reader = csv.reader(results, delimiter=',')
#         new_data = csv.DictReader(results)
#         old_data = csv.DictReader(results_old)
#
#         new_data = {row['name']: row for row in new_data}
#         old_data = {row['name']: row for row in old_data}
#
#         print(new_data)
#
#         for row in old_reader:
#             mol = Molecule()
#             mol.name = row[0]
#             mol.smiles = row[1]
#
#             try:
#                 mol.old_vap = float(row[2])
#                 mol.exp_vap = float(row[3])
#                 mol.old_dens = float(row[7])
#                 mol.exp_dens = float(row[8])
#             except ValueError:
#                 continue
#
#             try:
#                 mol.new_dens = float(new_data[mol.name]['density'])
#                 mol.new_vap = float(new_data[mol.name]['heat_of_vap'])
#             except KeyError:
#                 try:
#                     mol.new_dens = float(old_data[mol.name]['density'])
#                     mol.new_vap = float(old_data[mol.name]['heat_of_vap'])
#                 except KeyError:
#                     mol.new_dens = 0
#                     mol.new_vap = 0
#             mol.append_to_csv()
#
#
# class Molecule:
#
#     def __init__(self):
#
#         self.name = None
#         self.smiles = None
#
#         self.exp_vap = None
#         self.exp_dens = None
#         self.old_vap = None
#         self.old_dens = None
#         self.new_vap = None
#         self.new_dens = None
#
#     @staticmethod
#     def _calculate_error(exp, theor):
#         return abs(exp - theor) / exp * 100
#
#     def old_vap_error(self):
#         return self._calculate_error(self.exp_vap, self.old_vap)
#
#     def old_dens_error(self):
#         return self._calculate_error(self.exp_dens, self.old_dens)
#
#     def new_vap_error(self):
#         return self._calculate_error(self.exp_vap, self.new_vap)
#
#     def new_dens_error(self):
#         return self._calculate_error(self.exp_dens, self.new_dens)
#
#     def append_to_csv(self):
#
#         with open('final.csv', 'a') as final:
#             file_writer = csv.writer(final, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#             file_writer.writerow([
#                 self.name, self.smiles,
#                 self.exp_vap, self.old_vap, self.old_vap_error(), self.new_vap, self.new_vap_error(),
#                 self.exp_dens, self.old_dens, self.old_dens_error(), self.new_dens, self.new_dens_error()
#             ])
#
#
# if __name__ == '__main__':
#     parse_molecules()

class FreeParams:
    """Temporary class for interfacing with forcebalance"""

    def __init__(self, vfree, bfree, rfree):
        self.vfree = vfree
        self.bfree = bfree
        self.rfree = rfree


self.elem_dict = {
    'H': FreeParams(7.6, 6.5, 1.64),
    'B': FreeParams(46.7, 99.5, 2.08),
    'C': FreeParams(34.4, 46.6, 2.08),
    'N': FreeParams(25.9, 24.2, 1.72),
    'O': FreeParams(22.1, 15.6, 1.60),
    'F': FreeParams(18.2, 9.5, 1.58),
    'P': FreeParams(84.6, 185, 2.00),
    'S': FreeParams(75.2, 134.0, 2.00),
    'Cl': FreeParams(65.1, 94.6, 1.88),
    'Br': FreeParams(95.7, 162.0, 1.96),
    'Si': FreeParams(101.64, 305, 2.00),
}
"""
Run this script from inside the QUBEKit_<name>... folder to:
 - extract the molecule object
 - initialise LennardJones class
 - Update rfree params for each atom
 - Re-calculate the L-J parameters
 - Obtain a new xml with the updated parameters
"""
from QUBEKit.lennard_jones import LennardJones
from QUBEKit.utils.helpers import unpickle


molecule = unpickle()['finalise']

lj = LennardJones(molecule)
# Use Force Balance to update the L-J params
lj.elem_dict[??].rfree = ?

molecule.NonbondedForce = lj.calculate_non_bonded_force()

molecule.write_parameters()

