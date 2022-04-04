from shutil import rmtree
import numpy as np

from os import mkdir
from os.path import isdir

from cirrus.util.config import settings, logger


def create_folder_for_tiffs(path_level1, name):
    if not isdir(path_level1):
        mkdir(path_level1)
    if not isdir(f'{path_level1}/{name}'):
        mkdir(f'{path_level1}/{name}')


def get_time(raster):
    dt = raster.time.data
    return np.datetime_as_string(dt, unit='m').replace(':', '-')


def grADS2tiff(raster, name, coll_name, id_level=None):
    """_summary_

    Args:
        name (_type_): _description_
        coll_name (_type_): _description_
        file_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        
        raster = dataframe[name][0]
        file_date = get_time(raster)
        tifs_path = f'{settings.CEMPADIR}tifs'
        if isdir(tifs_path):
            rmtree(tifs_path)
        mkdir(tifs_path)
        
        path_level1 = f'{tifs_path}/{file_date}'
        create_folder_for_tiffs(path_level1, name)
        name_tif = f'{path_level1}/{name}/{coll_name}.tif'
        logger.debug(f'Criando tif {name_tif}')
        if isinstance(id_level, int):
            raster = raster.isel(lev=id_level).rio.set_spatial_dims(
                'lon', 'lat'
            )
        else:
            raster = raster.rio.set_spatial_dims('lon', 'lat')

        raster.rio.set_crs('epsg:4674')
        raster.rio.to_raster(name_tif)
        return True
    except:
        return False
