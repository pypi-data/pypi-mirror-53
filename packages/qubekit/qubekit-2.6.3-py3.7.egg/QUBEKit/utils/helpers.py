#!/usr/bin/env python3

from QUBEKit.utils import constants
from QUBEKit.utils.exceptions import PickleFileNotFound, QUBEKitLogFileNotFound

from collections import OrderedDict, namedtuple
from configparser import ConfigParser
from contextlib import contextmanager
import csv
import decimal
from importlib import import_module
import math
import operator
import os
import pickle

import numpy as np


class Configure:
    """
    Class to help load, read and write ini style configuration files returns dictionaries of the config
    settings as strings, all numbers must then be cast before use.
    """

    home = os.path.expanduser('~')
    config_folder = os.path.join(home, 'QUBEKit_configs')
    master_file = 'master_config.ini'

    qm = {
        'theory': 'B3LYP',              # Theory to use in freq and dihedral scans recommended e.g. wB97XD or B3LYP
        'basis': '6-311++G(d,p)',       # Basis set
        'vib_scaling': '1',         # Associated scaling to the theory
        'threads': '2',                 # Number of processors used in Gaussian09; affects the bonds and dihedral scans
        'memory': '2',                  # Amount of memory (in GB); specified in the Gaussian09 scripts
        'convergence': 'GAU_TIGHT',     # Criterion used during optimisations; works using PSI4, GeomeTRIC and G09
        'iterations': '350',            # Max number of optimisation iterations
        'bonds_engine': 'psi4',         # Engine used for bonds calculations
        'density_engine': 'g09',        # Engine used to calculate the electron density
        'charges_engine': 'chargemol',  # Engine used for charge partitioning
        'ddec_version': '6',            # DDEC version used by Chargemol, 6 recommended but 3 is also available
        'geometric': 'True',            # Use GeomeTRIC for optimised structure (if False, will just use PSI4)
        'solvent': 'True',              # Use a solvent in the PSI4/Gaussian09 input
    }

    fitting = {
        'dih_start': '-165',            # Starting angle of dihedral scan
        'increment': '15',              # Angle increase increment
        'dih_end': '180',               # The last dihedral angle in the scan
        't_weight': 'infinity',         # Weighting temperature that can be changed to better fit complicated surfaces
        'opt_method': 'BFGS',           # The type of SciPy optimiser to use
        'refinement_method': 'SP',      # The type of QUBE refinement that should be done SP: single point energies
        'tor_limit': '20',              # Torsion Vn limit to speed up fitting
        'div_index': '0',               # Fitting starting index in the division array
        'parameter_engine': 'xml',      # Method used for initial parametrisation
        'l_pen': '0.0',                 # The regularisation penalty
        'relative_to_global': 'False'   # If we should compute our relative energy surface
                                        # compared to the global minimum
    }

    excited = {
        'excited_state': 'False',       # Is this an excited state calculation
        'excited_theory': 'TDA',
        'nstates': '3',
        'excited_root': '1',
        'use_pseudo': 'False',
        'pseudo_potential_block': ''
    }

    descriptions = {
        'chargemol': '/home/<QUBEKit_user>/chargemol_09_26_2017',  # Location of the chargemol program directory
        'log': '999',                   # Default string for the working directories and logs
    }

    help = {
        'theory': ';Theory to use in freq and dihedral scans recommended wB97XD or B3LYP, for example',
        'basis': ';Basis set',
        'vib_scaling': ';Associated scaling to the theory',
        'threads': ';Number of processors used in g09; affects the bonds and dihedral scans',
        'memory': ';Amount of memory (in GB); specified in the g09 and PSI4 scripts',
        'convergence': ';Criterion used during optimisations; GAU, GAU_TIGHT, GAU_VERYTIGHT',
        'iterations': ';Max number of optimisation iterations',
        'bonds_engine': ';Engine used for bonds calculations',
        'density_engine': ';Engine used to calculate the electron density',
        'charges_engine': ';Engine used for charge partitioning',
        'ddec_version': ';DDEC version used by Chargemol, 6 recommended but 3 is also available',
        'geometric': ';Use geometric for optimised structure (if False, will just use PSI4)',
        'solvent': ';Use a solvent in the psi4/gaussian09 input',
        'dih_start': ';Starting angle of dihedral scan',
        'increment': ';Angle increase increment',
        'dih_end': ';The last dihedral angle in the scan',
        't_weight': ';Weighting temperature that can be changed to better fit complicated surfaces',
        'l_pen': ';The regularisation penalty',
        'relative_to_global': ';If we should compute our relative energy surface compared to the global minimum',
        'opt_method': ';The type of SciPy optimiser to use',
        'refinement_method': ';The type of QUBE refinement that should be done SP: single point energies',
        'tor_limit': ';Torsion Vn limit to speed up fitting',
        'div_index': ';Fitting starting index in the division array',
        'parameter_engine': ';Method used for initial parametrisation',
        'chargemol': ';Location of the Chargemol program directory (do not end with a "/")',
        'log': ';Default string for the names of the working directories',
        'excited_state': ';Use the excited state',
        'excited_theory': ';Excited state theory TDA or TD',
        'nstates': ';The number of states to use',
        'excited_root': ';The root',
        'use_pseudo': ';Use a pseudo potential',
        'pseudo_potential_block': ';Enter the pseudo potential block here eg'
    }

    def load_config(self, config_file='default_config'):
        """This method loads and returns the selected config file."""

        if config_file == 'default_config':

            # Check if the user has made a new master file to use
            if self.check_master():
                qm, fitting, excited, descriptions = self.ini_parser(os.path.join(self.config_folder, self.master_file))

            else:
                # If there is no master then assign the default config
                qm, fitting, excited, descriptions = self.qm, self.fitting, self.excited, self.descriptions

        else:
            # Load in the ini file given
            if os.path.exists(config_file):
                qm, fitting, excited, descriptions = self.ini_parser(config_file)

            else:
                qm, fitting, excited, descriptions = self.ini_parser(os.path.join(self.config_folder, config_file))

        # Now cast the numbers
        clean_ints = ['threads', 'memory', 'iterations', 'ddec_version', 'dih_start',
                      'increment', 'dih_end', 'tor_limit', 'div_index', 'nstates', 'excited_root']

        for key in clean_ints:

            if key in qm:
                qm[key] = int(qm[key])

            elif key in fitting:
                fitting[key] = int(fitting[key])

            elif key in excited:
                excited[key] = int(excited[key])

        # Now cast the one float the scaling
        qm['vib_scaling'] = float(qm['vib_scaling'])

        # Now cast the bools
        qm['geometric'] = True if qm['geometric'].lower() == 'true' else False
        qm['solvent'] = True if qm['solvent'].lower() == 'true' else False
        excited['excited_state'] = True if excited['excited_state'].lower() == 'true' else False
        excited['use_pseudo'] = True if excited['use_pseudo'].lower() == 'true' else False
        fitting['relative_to_global'] = True if fitting['relative_to_global'].lower() == 'true' else False

        # Now handle the weight temp
        if fitting['t_weight'] != 'infinity':
            fitting['t_weight'] = float(fitting['t_weight'])

        # Now cast the regularisation penalty to float
        fitting['l_pen'] = float(fitting['l_pen'])

        # return qm, fitting, descriptions
        return {**qm, **fitting, **excited, **descriptions}

    @staticmethod
    def ini_parser(ini):
        """Parse an ini type config file and return the arguments as dictionaries."""

        config = ConfigParser(allow_no_value=True)
        config.read(ini)
        qm = config.__dict__['_sections']['QM']
        fitting = config.__dict__['_sections']['FITTING']
        excited = config.__dict__['_sections']['EXCITED']
        descriptions = config.__dict__['_sections']['DESCRIPTIONS']

        return qm, fitting, excited, descriptions

    def show_ini(self):
        """Show all of the ini file options in the config folder."""

        # Hide the emacs backups
        return [ini for ini in os.listdir(self.config_folder) if not ini.endswith('~')]

    def check_master(self):
        """Check if there is a new master ini file in the configs folder."""

        return os.path.exists(os.path.join(self.config_folder, self.master_file))

    def ini_writer(self, ini):
        """Make a new configuration file in the config folder using the current master as a template."""

        # make sure the ini file has an ini ending
        if not ini.endswith('.ini'):
            ini += '.ini'

        # Set config parser to allow for comments
        config = ConfigParser(allow_no_value=True)

        categories = {
            'QM': self.qm,
            'FITTING': self.fitting,
            'EXCITED': self.excited,
            'DESCRIPTIONS': self.descriptions
        }

        for name, data in categories.items():
            config.add_section(name)
            for key, val in data.items():
                config.set(name, self.help[key])
                config.set(name, key, val)

        with open(os.path.join(self.config_folder, ini), 'w+') as out:
            config.write(out)

    def ini_edit(self, ini_file):
        """Open the ini file for editing in the command line using whatever program the user wants."""

        # Make sure the ini file has an ini ending
        if not ini_file.endswith('.ini'):
            ini_file += '.ini'

        ini_path = os.path.join(self.config_folder, ini_file)
        os.system(f'emacs -nw {ini_path}')


Colours = namedtuple('colours', 'red green orange blue purple end')

# Uses exit codes to set terminal font colours.
# \033[ is the exit code. 1;32m are the style (bold); colour (green) m reenters the code block.
# The second exit code resets the style back to default.
COLOURS = Colours(
    red='\033[1;31m',
    green='\033[1;32m',
    orange='\033[1;33m',
    blue='\033[1;34m',
    purple='\033[1;35m',
    end='\033[0m'
)


def mol_data_from_csv(csv_name):
    """
    Scan the csv file to find the row with the desired molecule data.
    Returns a dictionary of dictionaries in the form:
    {'methane': {'charge': 0, 'multiplicity': 1, ...}, 'ethane': {'charge': 0, ...}, ...}
    """

    with open(csv_name, 'r') as csv_file:

        mol_confs = csv.DictReader(csv_file)

        rows = []
        for row in mol_confs:

            # Converts to ordinary dict rather than ordered.
            row = dict(row)
            # If there is no config given assume its the default
            row['charge'] = int(float(row['charge'])) if row['charge'] else 0
            row['multiplicity'] = int(float(row['multiplicity'])) if row['multiplicity'] else 1
            row['config'] = row['config'] if row['config'] else 'default_config'
            row['smiles'] = row['smiles'] if row['smiles'] else None
            row['torsion_order'] = row['torsion_order'] if row['torsion_order'] else None
            row['restart'] = row['restart'] if row['restart'] else None
            row['end'] = row['end'] if row['end'] else 'finalise'
            rows.append(row)

    # Creates the nested dictionaries with the names as the keys
    final = {row['name']: row for row in rows}

    # Removes the names from the sub-dictionaries:
    # e.g. {'methane': {'name': 'methane', 'charge': 0, ...}, ...}
    # ---> {'methane': {'charge': 0, ...}, ...}
    for val in final.values():
        del val['name']

    return final


def generate_bulk_csv(csv_name, max_execs=None):
    """
    Generates a csv with name "csv_name" with minimal information inside.
    Contains only headers and a row of defaults and populates all of the named files where available.
    max_execs determines the max number of executions per csv file.
    For example, 10 pdb files with a value of max_execs=6 will generate two csv files,
    one containing 6 of those files, the other with the remaining 4.
    """

    if csv_name[-4:] != '.csv':
        raise TypeError('Invalid or unspecified file type. File must be .csv')

    # Find any local pdb files to write sample configs
    files = []
    for file in os.listdir("."):
        if file.endswith('.pdb'):
            files.append(file[:-4])

    # If max number of pdbs per file is unspecified, just put them all in one file.
    if max_execs is None:
        with open(csv_name, 'w') as csv_file:

            file_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(['name', 'charge', 'multiplicity', 'config', 'smiles', 'torsion_order', 'restart', 'end'])
            for file in files:
                file_writer.writerow([file, 0, 1, '', '', '', '', ''])
        print(f'{csv_name} generated.', flush=True)
        return

    try:
        max_execs = int(max_execs)
    except TypeError:
        raise TypeError('Number of executions must be provided as an int greater than 1.')
    if max_execs > len(files):
        raise ValueError('Number of executions cannot exceed the number of files provided.')

    # If max number of pdbs per file is specified, spread them across several csv files.
    num_csvs = math.ceil(len(files) / max_execs)

    for csv_count in range(num_csvs):
        with open(f'{csv_name[:-4]}_{str(csv_count).zfill(2)}.csv', 'w') as csv_file:
            file_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(['name', 'charge', 'multiplicity', 'config', 'smiles', 'torsion_order', 'restart', 'end'])

            for file in files[csv_count * max_execs: (csv_count + 1) * max_execs]:
                file_writer.writerow([file, 0, 1, '', '', '', '', ''])

        print(f'{csv_name[:-4]}_{str(csv_count).zfill(2)}.csv generated.', flush=True)


def append_to_log(message, msg_type='major'):
    """
    Appends a message to the log file in a specific format.
    Used for significant stages in the program such as when a stage has finished.
    """

    # Starting in the current directory walk back looking for the log file
    search_dir = os.getcwd()
    while 'QUBEKit_log.txt' not in os.listdir(search_dir):
        search_dir = os.path.split(search_dir)[0]
        if not search_dir:
            raise QUBEKitLogFileNotFound('Cannot locate QUBEKit log file.')

    log_file = os.path.abspath(os.path.join(search_dir, 'QUBEKit_log.txt'))

    # Check if the message is a blank string to avoid adding blank lines and unnecessary separators
    if message:
        with open(log_file, 'a+') as file:
            if msg_type == 'major':
                file.write(f'~~~~~~~~{message.upper()}~~~~~~~~')
            elif msg_type == 'warning':
                file.write(f'########{message.upper()}########')
            elif msg_type == 'minor':
                file.write(f'~~~~~~~~{message}~~~~~~~~')
            else:
                raise KeyError('Invalid message type; use major, warning or minor.')

            file.write(f'\n\n{"-" * 50}\n\n')


def pretty_progress():
    """
    Neatly displays the state of all QUBEKit running directories in the terminal.
    Uses the log files to automatically generate a matrix which is then printed to screen in full colour 4k.
    """

    # Find the path of all files starting with QUBEKit_log and add their full path to log_files list
    log_files = []
    for root, dirs, files in os.walk('.', topdown=True):
        for file in files:
            if 'QUBEKit_log.txt' in file and 'backups' not in root:
                log_files.append(os.path.abspath(f'{root}/{file}'))

    if not log_files:
        print('No QUBEKit directories with log files found. Perhaps you need to move to the parent directory.')
        return

    # Open all log files sequentially
    info = OrderedDict()
    for file in log_files:
        with open(file, 'r') as log_file:
            for line in log_file:
                if 'Analysing:' in line:
                    name = line.split()[1]
                    break
            else:
                # If the molecule name isn't found, there's something wrong with the log file
                # To avoid errors, just skip over that file and tell the user.
                print(f'Cannot locate molecule name in {file}\nIs it a valid, QUBEKit-made log file?\n')

        # Create ordered dictionary based on the log file info
        info[name] = populate_progress_dict(file)

    print('Displaying progress of all analyses in current directory.')
    print(f'Progress key: {COLOURS.green}\u2713{COLOURS.end} = Done;', end=' ')
    print(f'{COLOURS.blue}S{COLOURS.end} = Skipped;', end=' ')
    print(f'{COLOURS.red}E{COLOURS.end} = Error;', end=' ')
    print(f'{COLOURS.orange}R{COLOURS.end} = Running;', end=' ')
    print(f'{COLOURS.purple}~{COLOURS.end} = Queued')

    header_string = '{:15}' + '{:>10}' * 10
    print(header_string.format(
        'Name', 'Param', 'MM Opt', 'QM Opt', 'Hessian', 'Mod-Sem', 'Density', 'Charges', 'L-J', 'Tor Scan', 'Tor Opt'))

    # Sort the info alphabetically
    info = OrderedDict(sorted(info.items(), key=lambda tup: tup[0]))

    # Outer dict contains the names of the molecules.
    for key_out, var_out in info.items():
        print(f'{key_out[:13]:15}', end=' ')

        # Inner dict contains the individual molecules' data.
        for var_in in var_out.values():

            if var_in == u'\u2713':
                print(f'{COLOURS.green}{var_in:>9}{COLOURS.end}', end=' ')

            elif var_in == 'S':
                print(f'{COLOURS.blue}{var_in:>9}{COLOURS.end}', end=' ')

            elif var_in == 'E':
                print(f'{COLOURS.red}{var_in:>9}{COLOURS.end}', end=' ')

            elif var_in == 'R':
                print(f'{COLOURS.orange}{var_in:>9}{COLOURS.end}', end=' ')

            elif var_in == '~':
                print(f'{COLOURS.purple}{var_in:>9}{COLOURS.end}', end=' ')

        print('')


def populate_progress_dict(file_name):
    """
    With a log file open:
        Search for a keyword marking the completion or skipping of a stage;
        If that's not found, look for error messages,
        Otherwise, just return that the stage hasn't finished yet.
    Key:
        tick mark: Done; S: Skipped; E: Error; ~ (tilde): Not done yet, no error found.
    """

    # Indicators in the log file which show a stage has completed
    search_terms = ('PARAMETRISATION', 'MM_OPT', 'QM_OPT', 'HESSIAN', 'MOD_SEM', 'DENSITY', 'CHARGE', 'LENNARD',
                    'TORSION_S', 'TORSION_O')

    progress = OrderedDict((term, '~') for term in search_terms)

    restart_log = False

    with open(file_name) as file:
        for line in file:

            # Reset progress when restarting (set all progress to incomplete)
            if 'Continuing log file' in line:
                restart_log = True

            # Look for the specific search terms
            for term in search_terms:
                if term in line:
                    # If you find a search term, check if it's skipped (S)
                    if 'SKIP' in line:
                        progress[term] = 'S'
                    # If we have restarted then we need to
                    elif 'STARTING' in line:
                        progress[term] = 'R'
                    # If its finishing tag is present it is done (tick)
                    elif 'FINISHING' in line:
                        progress[term] = u'\u2713'

            # If an error is found, then the stage after the last successful stage has errored (E)
            if 'Exception Logger - ERROR' in line:
                # On the rare occasion that the error occurs after torsion optimisation (the final stage),
                # a try except is needed to catch the index error (because there's no stage after torsion_optimisation).
                for key, value in progress.items():
                    if value == 'R':
                        restart_term = search_terms.index(key)
                        progress[key] = 'E'
                        break

    if restart_log:
        for term, stage in progress.items():
            # Find where the program was restarted from
            if stage == 'R':
                restart_term = search_terms.index(term)
                break
        else:
            # If no stage is running, find the first stage that hasn't started; the first `~`
            for term, stage in progress.items():
                if stage == '~':
                    restart_term = search_terms.index(term)
                    break

        # Reset anything after the restart term to be `~` even if it was previously completed.
        try:
            for term in search_terms[restart_term + 1:]:
                progress[term] = '~'
        except UnboundLocalError:
            pass

    return progress


def pretty_print(molecule, to_file=False, finished=True):
    """
    Takes a ligand molecule class object and displays all the class variables in a clean, readable format.

    Print to log: * On exception
                  * On completion
    Print to terminal: * On call
                       * On completion

    Strictly speaking this should probably be a method of ligand class as it explicitly uses ligand's custom
    __str__ method with an extra argument.
    """

    pre_string = f'\n\nOn {"completion" if finished else "exception"}, the ligand objects are:'

    # Print to log file rather than to terminal
    if to_file:
        log_location = os.path.join(getattr(molecule, 'home'), 'QUBEKit_log.txt')
        with open(log_location, 'a+') as log_file:
            log_file.write(f'{pre_string.upper()}\n\n{molecule.__str__()}')

    # Print to terminal
    else:
        print(pre_string)
        # Custom __str__ method; see its documentation for details.
        print(molecule.__str__(trunc=True))
        print('')


def unpickle(location=None):
    """
    Function to unpickle a set of ligand objects from the pickle file, and return a dictionary of ligands
    indexed by their progress.
    """

    mol_states = OrderedDict()

    # unpickle the pickle jar
    # try to load a pickle file make sure to get all objects
    pickle_file = '.QUBEKit_states'
    if location is not None:
        pickle_path = os.path.join(location, pickle_file)

    else:
        search_dir = os.getcwd()
        while pickle_file not in os.listdir(search_dir):
            search_dir = os.path.split(search_dir)[0]
            if not search_dir:
                raise PickleFileNotFound('Pickle file not found; have you deleted it?')

        pickle_path = os.path.join(search_dir, pickle_file)

    with open(pickle_path, 'rb') as jar:
        while True:
            try:
                mol = pickle.load(jar)
                mol_states[mol.state] = mol
            except EOFError:
                break

    return mol_states


def display_molecule_objects(*names):
    """
    prints the requested molecule objects in a nicely formatted way, easy to copy elsewhere.
    :param names: list of strings where each item is the name of a molecule object such as 'basis' or 'coords'
    """
    try:
        molecule = unpickle()['finalise']
    except KeyError:
        print('QUBEKit encountered an error during execution; returning the initial molecule objects.')
        molecule = unpickle()['parametrise']

    for name in names:
        result = getattr(molecule, name, None)
        if result is not None:
            print(f'{name}:  {repr(result)}')
        else:
            print(f'Invalid molecule object: {name}. Please check the log file for the data you require.')


@contextmanager
def assert_wrapper(exception_type):
    """
    Makes assertions more informative when an Exception is thrown.
    Rather than just getting 'AssertionError' all the time, an actual named exception can be passed.
    Can be called multiple times in the same 'with' statement for the same exception type but different exceptions.

    Simple example use cases:

        with assert_wrapper(ValueError):
            assert (arg1 > 0), 'arg1 cannot be non-positive.'
            assert (arg2 != 12), 'arg2 cannot be 12.'
        with assert_wrapper(TypeError):
            assert (type(arg1) is not float), 'arg1 must not be a float.'
    """

    try:
        yield
    except AssertionError as exc:
        raise exception_type(*exc.args)


def check_symmetry(matrix, error=1e-5):
    """Check matrix is symmetric to within some error."""

    # Check the matrix transpose is equal to the matrix within error.
    with assert_wrapper(ValueError):
        assert (np.allclose(matrix, matrix.T, atol=error)), 'Matrix is not symmetric.'

    print(f'{COLOURS.purple}Symmetry check successful. '
          f'The matrix is symmetric within an error of {error}.{COLOURS.end}')
    return True


def check_net_charge(charges, ideal_net=0, error=1e-5):
    """Given a list of charges, check if the calculated net charge is within error of the desired net charge."""

    # Ensure total charge is near to integer value:
    total_charge = sum(atom for atom in charges)

    with assert_wrapper(ValueError):
        assert (abs(total_charge - ideal_net) < error), ('Total charge is not close enough to desired '
                                                         'integer value in configs.')

    print(f'{COLOURS.purple}Charge check successful. '
          f'Net charge is within {error} of the desired net charge of {ideal_net}.{COLOURS.end}')
    return True


def collect_archive_tdrive(tdrive_record, client):
    """
    This function takes in a QCArchive tdrive record and collects all of the final geometries and energies to be used in
    torsion fitting.
    :param client:  A QCPortal client instance.
    :param tdrive_record: A QCArchive data object containing an optimisation and energy dictionary
    :return: QUBEKit qm_scans data: list of energies and geometries [np.array(energies), [np.array(geometry)]]
    """

    # Sort the dictionary by ascending keys
    energy_dict = {int(key.strip('][')): value for key, value in tdrive_record.final_energy_dict.items()}
    sorted_energies = sorted(energy_dict.items(), key=operator.itemgetter(0))

    energies = np.array([x[1] for x in sorted_energies])

    geometry = []
    # Now make the optimization dict and store an array of the final geometry
    for pair in sorted_energies:
        min_energy_id = tdrive_record.minimum_positions[f'[{pair[0]}]']
        opt_history = int(tdrive_record.optimization_history[f'[{pair[0]}]'][min_energy_id])
        opt_struct = client.query_procedures(id=opt_history)[0]
        geometry.append(opt_struct.get_final_molecule().geometry * constants.BOHR_TO_ANGS)
        assert opt_struct.get_final_energy() == pair[1], "The energies collected do not match the QCArchive minima."

    return [energies, geometry]


def set_net(values, net=0, dp=6):
    """
    Take a list of values and make sure the sum is equal to net to the required dp
    If they are not, add the extra to the final value in the list.
    :param values: list of values
    :param net: the desired total of the list
    :param dp: the number of decimal places required
    :return: the list of updated values with the correct net value
    """

    decimal.getcontext().prec = dp
    new_values = [decimal.Decimal(str(val)) for val in values]
    extra = net - sum(new_values)
    if extra:
        new_values[-1] += extra

    return new_values


def make_and_change_into(name):
    """
    - Attempt to make a directory with name <name>, don't fail if it exists.
    - Change into the directory.
    """

    try:
        os.mkdir(name)
    except FileExistsError:
        pass
    finally:
        os.chdir(name)


def missing_import(name, fail_msg=''):
    """
    Generates a class which raises an import error when initialised.
    e.g. SomeClass = missing_import('SomeClass') will make SomeClass() raise ImportError
    """
    def init(self, *args, **kwargs):
        raise ImportError(
            f'The class {name} you tried to call is not importable; '
            f'this is likely due to it not doing installed.\n\n'
            f'{f"Fail Message: {fail_msg}" if fail_msg else ""}'
        )
    return type(name, (), {'__init__': init})


def try_load(engine, module):
    """
    Try to load a particular engine from a module.
    If this fails, a dummy class is imported in its place with an import error raised on initialisation.

    :param engine: Name of the engine (PSI4, OpenFF, ONETEP, etc).
    :param module: Name of the QUBEKit module (.psi4, .openff, .onetep, etc).
    :return: Either the engine is imported as normal, or it is replaced with dummy class which
    just raises an import error with a message.
    """
    try:
        module = import_module(module, __name__)
        return getattr(module, engine)
    except (ModuleNotFoundError, AttributeError) as exc:
        print(f'{COLOURS.orange}Warning, failed to load: {engine}; continuing for now.\nReason: {exc}{COLOURS.end}\n')
        return missing_import(engine, fail_msg=str(exc))
