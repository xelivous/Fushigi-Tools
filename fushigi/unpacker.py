import os, png, io
from .util import * # in package
import logging as log

# todo
def unpack(file_handler, format, metadata, asset_dir):
    f = file_handler
    f.seek(0) #make sure we're at start
    
    if format == 'Him5':
        index = 0
        for folder in metadata:
            index += 1
            folder_dir = os.path.join(asset_dir, str(index).zfill(3))
            ensure_dir_exists(folder_dir)
            
            for fil in folder['files']:
                file_path = os.path.join(folder_dir, fil['filename'])
                f.seek(fil['data']['contents_offset'])
                data = f.read(fil['data']['length'])
                
                with open(file_path, 'wb') as file_opened:
                    file_opened.write(data)
                
    pass