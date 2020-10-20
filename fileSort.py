""" File Sorter Module
This module sorts files inside certain directories (e.g Downloads) into their respective folder in HOME

* Add more sortable directories to the file through the directories variable
* Add more sortable formats to the file through modification of formats variable 

This file is licensed under the MIT License (See LICENSE for more info)
"""
import os

home = os.getenv("HOME")

# List of directories to run the module on
directories = [
    home,
    os.path.join(home, 'Downloads'),
]

# Known formats that must be sorted
# Custom Folders specified must exist
formats = {
    # e.g: 'Folder': ('.fmt1', '.fmt2')
    'Pictures': ('.jpg', '.jpeg', '.png', '.webp', '.epub'),
    'Videos': ('.mp4', '.mkv', '.webm'),
    'Documents': ('.pdf', '.xlsx', '.csv', '.epub', '.xls'),
    'Music': ('.mp3', ),
    # Custom Folders
    'Archives': ('.tar.gz', '.tar.xz', '.tar', '.zip', '.gz', '.7z', '.rar'), 
    'Packages': ('.deb', '.exe', )
}

for directory in directories:
    current, folders, files = next(os.walk(directory)) # Generates a separeted list of folders and files 
    for file in files:
        origin = os.path.join(current, file)
        for destination, fmt in formats.items():
             if file.endswith(fmt):
                 os.rename(origin, os.path.join(home, destination, file))
                 break
