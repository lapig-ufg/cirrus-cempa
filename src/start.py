
from shutil import rmtree
from os.path import isdir
from os import mkdir
from datetime import datetime
from dynaconf import Dynaconf
from cirrus.grADS2db import to_db

from cirrus.model import clear_tables
#from cirrus.netcdf2postgis import main
from cirrus.util.config import logger, settings
from cirrus.dowloads import downloads_files

initial_config = Dynaconf(
    envvar_prefix='CEMPA',
    settings_files=['settings.toml', '.secrets.toml'],
)

def main():
    logger.info(f'Numero de pool {initial_config.N_POOL}')

    _start = datetime.now()
    #if downloads_files():
    logger.info('indo limpar o banco Banco linado')
    clear_tables()
    logger.info('Banco linado')
        #Create cempa_tifs
    tifs_path = f'{settings.CATALOG}cempa_tifs'
        if isdir(tifs_path):
            rmtree(tifs_path)
    mkdir(tifs_path)

    meta_path = f'{settings.CATALOG}cempa_metadata'
    #    if isdir(meta_path):
    #        rmtree(meta_path)
    #mkdir(meta_path)

    to_db()
    #else:
    #    pass
    logger.info(f'Fim Time:{datetime.now() - _start}')

if __name__ == '__main__':
    main()
