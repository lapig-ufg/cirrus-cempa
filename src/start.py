
from dynaconf import Dynaconf
from cirrus.grADS2db import to_db

#from cirrus.model import clear_tables
#from cirrus.netcdf2postgis import main
from cirrus.util.config import logger
from cirrus.dowloads import downloads_files

initial_config = Dynaconf(
    envvar_prefix='CEMPA',
    settings_files=['settings.toml', '.secrets.toml'],
)

def main():
    logger.info(f'Numero de pool {initial_config.N_POOL}')
    #if downloads_files():
        #clear_tables()
    to_db()
    #else:
    #    pass
    #main(initial_config.FORCE_SAVE_BD)


if __name__ == '__main__':
    main()
