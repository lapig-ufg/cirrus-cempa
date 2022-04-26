from cirrus.util.functions import creat_titles
from cirrus.util.config import settings, logger

from os.path import isdir
from os import mkdir

from glob import glob


def creat_title_all_file():
    files =  [file.replace('_color.tif','') for file in glob(f'{settings.CATALOG}/cempa_tifs/*/*/*_color.tif')]
    total_files = len(files)
    for n, file in enumerate(files):
        logger.debug('Criando title do file {file} {n}/{total_files}')
        if not isdir(file):
            mkdir(file)
            creat_titles(file,22)




