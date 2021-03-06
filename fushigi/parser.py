from .util import * # in package
import logging as log

def file_info(file_handler):
    f = file_handler

    # Format
    log.info('file format start: 0x%08X', f.tell())
    file_format = f.read(4).decode('utf-8')
    log.debug('file format: %s', file_format)

    if file_format == 'Him5':
        # Folders
        log.info('folder start: 0x%08X', f.tell())
        folder_count = read_int(f)
        log.debug('folder count: %s', folder_count)
        folders = []
        for i in range(folder_count):
            folders.append({
                'size': read_int(f),
                'offset': read_int(f),
                'files': []
            })
        log.debug('folders: %s', folders)

        # Files
        log.info('file start: 0x%08X', f.tell())
        for folder in folders:
            folder_size = folder['size']
            if folder_size > 0:
                data = read_chunk(folder['offset'], folder_size, f)
                while data.tell() < folder_size - 1:
                    folder['files'].append({
                        'info_length': read_byte(data), # relatively useless, but i'll return it anyway
                        'offset': read('>I', 4, data), # big endian because why the fuck not
                        'filename': read_null_term_string(data),
                        'data': []
                    })
                    align(2, f)
        log.debug('completed folders: %s', folders)

        for folder in folders:
            for fil in folder['files']:
                f.seek(fil['offset'])
                file_length = read('<I', 4, f)
                file_unknown = read('<I', 4, f)
                contents_offset = f.tell() # basically fil['offset'] + 8..., which matches up with the next file's start usually
                
                #log.info('file: %s | offset: %s | length: %s | unknown: %s', fil['filename'], fil['offset'], file_length, file_unknown)
                fil['data'] = {
                    'length': file_length,
                    'unknown': file_unknown,
                    'contents_offset': contents_offset
                }

                
                
                
        
    else:
        log.error('unsupported file format: %s', file_format)

    return file_format, folders
