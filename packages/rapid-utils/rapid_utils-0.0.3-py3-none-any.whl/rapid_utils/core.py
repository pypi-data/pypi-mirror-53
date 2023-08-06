import requests
import uuid
from urllib.parse import unquote
import json
import os, re

def get_extension(filename):
    '''
    returns extension of filename

    Args:
        filename (str): filename
    Returns:
        extension (str): returns extension in lowercase
    '''
    return filename.rsplit('.', 1)[1]

def is_allowed_extension(filename, formats):
    '''
    checks whether filename extension is in formats

    Args:
        filename (str): filename
        formats (list): list of extensions

    Returns:
        bool: True if filename extension is in formats, False otherwise

    Examples:
        >>> is_allowed_extension('video.mp4', ['mp4', '3gp', 'mkv'])
        True
        >>> is_allowed_extension('video.mp4', ['zip', 'tar'])
        False
    '''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in formats


def allowed_file(filename, formats):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in formats

def download_file(url, dirname=".", add_prefix=False):
    '''
    downloads files from url

    Args:
        url (str): url
        dirname (str): directory name in which file will be downloading
        add_prefix (bool): adds uuid as prefix to filename if True, nothing otherwise

    Returns:
        filename (str): returns filepath
    '''
    if add_prefix:
        filename = unquote(os.path.sep.join([dirname, uuid.uuid1().hex + url.split("/")[-1]]))
    else:
        filename = unquote(os.path.sep.join([dirname, url.split("/")[-1]]))
    file = requests.get(url, stream=True)
    with open(filename,"wb") as f:
        for chunk in file.iter_content(chunk_size=512 * 1024): 
            if chunk:
                f.write(chunk)
    return filename

def is_json(string=None, path=None):
    try:
        if string:
            json.loads(string)
            return True
        if path:
            json.load(open(path, "r"))
            return True
    except:
        return False

def get_json_from_url(url):
    return requests.get(url).json()

def get_file_size(filepath, unit='MB'):
    filesize = os.path.getsize(filepath)#v /1000/1000, ".2f"))
    return format(float({
        'byte': filesize,
        'kb': filesize/1000,
        'mb': filesize/1000/1000,
        'gb': filesize/1000/1000/1000,
        'tb': filesize/1000/1000/1000/1000
    }[unit.lower()]), ".2f")

def validate_bundle_identifier(bundle_identifier):
    ''' This method follows google play standards for bundle identifier validation
    Rules:
        1. It must have at least two segments (one or more dots).
        2. Each segment must start with a letter.
        3. All characters must be alphanumeric or an underscore [a-zA-Z0-9_]
    '''
    segments = bundle_identifier.split(".")
    print(segments)
    if len(segments) < 2:
        return False, 'bundle identifier must have atleast a dot'
    if '' in segments:
        return False, 'In bundle identifier, each segment must start with a letter after .'
    
    for segment in segments:
        if not re.match("^[a-zA-Z]+.*", segment):
            return False, 'In bundle identifier, each segment must start with a letter'
        if not (segment.strip().isalpha() or '_' in segment):
            return False, 'In bundle identifier, each segment must be alphanumeric'
    return True, 'valid bundle identifier'

def is_bundle_identifier_registered(bundle_identifier):
    url = 'https://play.google.com/store/apps/details?id={}'.format(bundle_identifier)
    res = requests.get(url)
    if res.ok:
        return True, '{} bundle identifier already registered'.format(bundle_identifier)
    return False, '{} bundle identifier is available'.format(bundle_identifier)