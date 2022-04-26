import time
from datetime import datetime
from os import mkdir
from os.path import isdir
from shutil import rmtree
from glob import glob
from requests import post

from cirrus.dowloads import downloads_files
from cirrus.grADS2db import to_db
from cirrus.model import clear_tables
from cirrus.util.cach_make import run
# from cirrus.netcdf2postgis import main
from cirrus.util.config import logger, send_emai, settings
from cirrus.util.functions import creat_titles
from multiprocessing import Pool


def clear_dir():
    tifs_path = f'{settings.CATALOG}cempa_tifs'
    if isdir(tifs_path):
        rmtree(tifs_path)
    mkdir(tifs_path)
    color_bar = f'{settings.CATALOG}colorbar'
    if isdir(color_bar):
        rmtree(color_bar)
    mkdir(color_bar)
    meta_path = f'{settings.CATALOG}cempa_metadata'
    if isdir(meta_path):
        rmtree(meta_path)
    mkdir(meta_path)



def ows(layer):
    logger.log('CEMPA', f'reiniciando o server ows')
    restart_ows = post(settings.CEMPA_OWS_URL)
    logger.log('CEMPA', f'ows foi reiniciado')
    if restart_ows.status_code == 204:
        time.sleep(60)
        if isdir(settings.OWS_CACH):
            try:
                rmtree(settings.OWS_CACH)
            except Exception:
                logger.exception('Error ao limpar o cach')
        logger.log('CEMPA', f'ows reiniciado e cach limpo')
        time.sleep(60)
        logger.log('CEMPA', f'inicinado criacao do cach')
        run(layer)

def creat_title_all_file():
    files =  [file.replace('_color.tif','') for file in glob(f'{settings.CATALOG}cempa_tifs/*/*/*_color.tif')]
    total_files = len(files)
    for n, file in enumerate(files,1):
        #logger.debug(f'Criando title do file {file} {n}/{total_files}')
        if not isdir(file):
            mkdir(file)

    with Pool(22) as work:
        work.map(creat_titles, files)

def main():
    logger.info(f'Numero de pool {settings.N_POOL}')
    logger.log('CEMPA', 'Startd cirrus')
    _start = datetime.now()
    if True:#downloads_files():
        logger.info(f'Tempo de Dowload Time:{datetime.now() - _start}')
        logger.info('iniciando a limpesa do banco Banco linado')
        #clear_tables()
        logger.info('Banco limpo')
        # Create cempa_tifs
        #clear_dir()


        #layer = to_db()
        logger.debug('Chamando ows function')
        #ows(layer)

        _start_title = datetime.now()
        logger.log('CEMPA', 'Iniciando o gerador de title')
        creat_title_all_file()
        logger.log('CEMPA', f'end titles Time:{datetime.now() - _start_title}')





    # else:
    #    pass
    logger.log('CEMPA', f'end cirrus Time:{datetime.now() - _start}')
    send_emai()


if __name__ == '__main__':
    main()
