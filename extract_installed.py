""" Extract a list of all packages installed from shell history

This module goes through the files of shell history and extracts all packages installed from install commands
Currently, this module supports both bash and zsh history, make an issue for expansion.

Note: Use of bash operators (&, |, ;) is currently unsupported, commands with such characters are skipped
"""
import os 
import re

home = os.getenv("HOME")

PREFIX_LIST = {
    'apt': ['/usr/bin/apt', 'apt install'],
    'snap': ['/usr/bin/snap', 'snap install'],
    'yum': ['/usr/bin/yum', 'yum install'],
    'rpm': ['/usr/bin/rpm', 'rpm -i'],
}


ZSH_CLEANUP = re.compile(r': \d+:\d+;')

class Processor:
    """ Handles file operation and filtering """
    unsupported_operators = ['&', '|', ';', './']
    def __init__(self, prefixes):
        self.prefixes = prefixes
        self.packages = {}
        for manager in prefixes:
            self.packages[manager] = set()

    def _openFile(self, file_path):
        try:
            self.active = True
            self.file = open(file_path, 'r+', errors='ignore')
        except FileNotFoundError:
            self.active = False
            self.file = {}
    
    def invoke(self, file_path, processor_function, cleanup_function=None):
        self._openFile(file_path)
        if not self.active:
            return 
        for line in self.file:
            # Find the prefix used
            prefix = None
            for manager, values in prefixes.items():
                if values[1] in line:
                    prefix = values[1]
                    manager = manager
                    break
            if prefix is None:
                continue

            if cleanup_function is not None:
                line = cleanup_function(line)
            if any(operator in line for operator in self.unsupported_operators):
                continue

            line = line.replace('\n', '')
            self.packages[manager].update(processor_function(line, prefix))
        
        self.packages[manager].remove('') if '' in self.packages[manager] else None
        self.file.close()



def simpleProcessor(line, prefix):
    """ Processes a simple history (e.g .bash_history)

    a simple history is defined as a type of history file that contains nothing but one command in each line
    """
    return line.replace(prefix, '').split(' ')


def zshCleanup(line):
    return ZSH_CLEANUP.sub('', line)


def getAvailablePrefixes():
    prefixes = {}
    for key, values in PREFIX_LIST.items():
        if not os.path.exists(values[0]):
            continue
        if os.getenv('USER') != 'root':
            values[1] = 'sudo ' + values[1]
        prefixes[key] = values
    return prefixes


SHELL_LIST = {
    'bash': ['/bin/bash', os.path.join(home, '.bash_history'), simpleProcessor],
    'zsh':  ['/bin/zsh', os.path.join(home, '.zsh_history'), simpleProcessor, zshCleanup],
}

if __name__ == "__main__":
    prefixes = getAvailablePrefixes()
    p = Processor(prefixes)

    for key, values in SHELL_LIST.items():
        if os.path.exists(values[0]):
            p.invoke(*values[1:])
        else:
            print('{} not found, skipping...'.format(key))
    
    for manager, packages in p.packages.items():
        print('Installed via {}:'.format(manager), ' '.join(packages))
    
    # Favorite Picking
    choice = input('\nPick favorite packages? (y/n) [n]: ')
    favorite_enabled = False if choice != 'y' else True
    if favorite_enabled:
        favorites = {}
        default = input('Select default option (y/n) [n]: ')
        default = default if default != '' else 'n'
        for manager, packages in p.packages.items():
            print('{} packages:'.format(manager))
            favorite_packages = []
            try:
                for package in packages:
                    i = input('Keep {}? (y/n) [{}] '.format(package, default))
                    if (i == '' and default == 'y') or i == 'y':
                        favorite_packages.append(package)
            except KeyboardInterrupt:
                print('\n')
                continue
            finally:
                if favorite_packages:
                    favorites[manager] = favorite_packages
        
        for manager, packages in favorites.items():
            print('Install via {}:'.format(manager), ' '.join(packages))
    
    # Generate files
    picked_packages = p.packages if not favorite_enabled else favorites
    generate = input('Generate a sh file? (y/n) [y]: ') 
    generate_enabled = False if generate == 'n' else True

    if generate_enabled:
        with open('install.sh', 'w+') as file:
            file.write('echo "This file needs root access to run, make sure you have proper access"\n')
            for manager,  packages in picked_packages.items():
                file.write('{} {}\n'.format(PREFIX_LIST[manager][1], ' '.join(packages)))        