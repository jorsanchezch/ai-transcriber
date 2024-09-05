import base64
import mimetypes
import os

from .constants import EXCEL_MIME, EXCEL_EXTS, AUDIO_EXTS
from werkzeug.utils import secure_filename

def is_type(file, target_exts, target_mime_type):
    return file.filename.endswith(target_exts) and file.content_type.startswith(target_mime_type)
    
def is_audio(file):
    return is_type(file, AUDIO_EXTS, 'audio')

def is_excel(file):
    return is_type(file, EXCEL_EXTS, EXCEL_MIME)

def is_empty(row):
    return all(cell in [None, ""] for cell in row)

def file_dir(filename, root, temp=False):
    subdir = 'temp' if temp else ''
    return os.path.join(root, 'files', subdir, secure_filename(filename))

def save_file(file, root, temp=False):
    return file.save(file_dir(file.filename, root, temp))

def save_new_file(stream, filename, root, temp=False):
    path = file_dir(filename, root, temp)
    with open(path, 'wb') as f:
        f.write(stream.read())
        
    return path

def normalize_string(s):
    return s.strip().lower().replace(' ', '_')

def match_strings(str1, str2):
    return normalize_string(str1) == normalize_string(str2)