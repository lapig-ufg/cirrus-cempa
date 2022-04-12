
from shutil import rmtree
from os.path import isdir
from os import mkdir
from datetime import datetime
from dynaconf import Dynaconf
from cirrus.grADS2db import to_db
from requests import post

from cirrus.model import clear_tables
#from cirrus.netcdf2postgis import main
from cirrus.util.config import logger, settings, send_emai
from cirrus.dowloads import downloads_files

initial_config = Dynaconf(
    envvar_prefix='CEMPA',
    settings_files=['settings.toml', '.secrets.toml'],
)

def main():
    logger.info(f'Numero de pool {initial_config.N_POOL}')
    send_emai('Startd cirrus')
    _start = datetime.now()
    if downloads_files():
        logger.info(f'Tempo de Dowload Time:{datetime.now() - _start}')
        logger.info('iniciando a limpesa do banco Banco linado')
        clear_tables()
        logger.info('Banco limpo')
            #Create cempa_tifs
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

        to_db()

        restart_ows = post(initial_config.CEMPA_OWS_URL)
        if restart_ows.status_code == 204:
            if isdir(initial_config.OWS_CACH):
                rmtree(initial_config.OWS_CACH)
            send_emai(f'ows reiniciado e cach limpo')
    #else:
    #    pass
    send_emai(f'end cirrus Time:{datetime.now() - _start}')

if __name__ == '__main__':
    main()
