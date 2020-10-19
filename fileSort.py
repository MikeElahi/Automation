""" File Sorter
Sorts files from my home directory and Downloads folder to their appropriate respective folders

Note: This module uses two non-default folders 'Archives' and 'Packages' in your home directory for file storage.
"""
import os

home = os.environ["HOME"]

directories = [
    home,
    '{}/Downloads'.format(home),
]

formats = {
    'image': ('.jpg', '.jpeg', '.png', '.webp', '.epub'),
    'video': ('.mp4', '.mkv', '.webm'),
    'document': ('.pdf', '.xlsx', '.csv', '.epub', '.xls'),
    'music': ('.mp3', ),
    'archive': ('.tar.gz', '.tar.xz', '.tar', '.zip', '.gz', '.7z', '.rar'),
    'package': ('.deb', '.exe', )
}
for directory in directories:
    current, folders, files = next(os.walk(directory)) # Generates a separeted list of folders and files 
    
    for file in files:
        location = '{current}/{file}'.format(current=current, file=file)
        location.replace('//', '/')
        # Sort images into HOME/Pictures
        if file.endswith(formats['image']):
            os.rename(location, '{home}/Pictures/{file}'.format(home=home, file=file))
        # Sort videos into HOME/Videos
        if file.endswith(formats['video']):
            os.rename(location, '{home}/Videos/{file}'.format(home=home, file=file))
        # Sort documents into HOME/Documents
        if file.endswith(formats['document']):
            os.rename(location, '{home}/Documents/{file}'.format(home=home, file=file))
        # Sort music into HOME/Muisc
        if file.endswith(formats['music']):
            os.rename(location, '{home}/Music/{file}'.format(home=home, file=file))
        # Sort archives into HOME/Archives (I made this)
        if file.endswith(formats['archive']):
            os.rename(location, '{home}/Archives/{file}'.format(home=home, file=file))
        # Sort packages into HOME/Packages
        if file.endswith(formats['package']):
            os.rename(location, '{home}/Packages/{file}'.format(home=home, file=file))