NEW_FOLDERS = {
    'images': [],
    'video': [],
    'audio': [],
    'documents': [],
    'archives': []
}

IGNORE_FOLDERS = {'archives', 'video', 'audio', 'documents', 'images'}

EXTENSIONS = {
    'images': ['JPEG', 'PNG', 'JPG', 'SVG', 'HEIC', 'ICO'],
    'video': ['AVI', 'MP4', 'MOV', 'MKV', 'GIF'],
    'audio': ['MP3', 'OGG', 'WAV', 'AMR', 'FLAC'],
    'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
    'archives': ['ZIP', 'GZ', 'TAR'],
    'unknown': []
}

known_list = set()
unknown_list = set()
only_folders = []