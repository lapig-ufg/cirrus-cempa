import os
from datetime import datetime
from glob import glob
from os.path import isdir, isfile
import gdal2tiles

import seaborn as sns
from matplotlib import pyplot as plt

from cirrus.util.color import color
from cirrus.util.config import logger, variables
from cirrus.util.db import create_session
from PIL import ImageColor
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap

def colobar_convert(n, start, end, _len_color):
    return f'{((end - start) / _len_color) * n + start:.1f}'


def view_colormap(fname, my_cmap,start, end,type_var=''):
    plt.rc('ytick', labelsize=16)
    fig, ax = plt.subplots(figsize=(0.5, 16))
    fig.subplots_adjust(bottom=0.5)

    cmap = LinearSegmentedColormap.from_list("",my_cmap)
    
    step = 1
    if end < 1.01:
      #start = start * 100
      #end = end * 100
      step = 0.01
    norm = mpl.colors.Normalize(vmin=start, vmax=end)
    cb1 = mpl.colorbar.ColorbarBase(
        ax, 
        cmap=cmap,
       #boundaries=np.arange(start,end,step),
        norm=norm,
        orientation='vertical',
        #extend='both',
        #extendfrac='auto'
        )

    cb1.set_label(type_var, fontsize=16)
    plt.savefig(fname, dpi=300, transparent=True, bbox_inches='tight')
    




def get_time(name: str, return_txt=False) -> str:
    date_time_str = (
        name.split('/')[-1].replace('Go05km-A-', '').replace('00-g1.nc', '')
    )
    if return_txt:
        return date_time_str.replace('-', '')
    return str(datetime.strptime(date_time_str, '%Y-%m-%d-%H%M%S'))


def get_list_nc(path_files: str):
    return glob(f'{path_files}/*.nc')


def get_min_max(coll_table, table_name):
    try:
        _min, _max = session.execute(
            f'select min({coll_table}), max({coll_table}) from {table_name}'
        ).all()[0]
        return (round(_min, 2), round(_max + 0.05, 2))
    except:
        return (0, 1)


def exists_in_the_bank(file_hash: str):
    session = create_session()
    try:
        is_valid = (
            session.query(FileHash).filter_by(file_hash=file_hash).first()
        )
        if is_valid.file_hash == file_hash:
            return True
        return False
    except AttributeError:
        return False
    except:
        logger.exception('Error exists_in_the_bank')
        return True


def save_hash(str_hash: str) -> None:
    session = create_session()
    session.add(FileHash(file_hash=str_hash))
    session.commit()


def get_pallet(_min, _max, name):
    _color = variables[name]['color']
    _convert = variables[name]['convert']
    _len_cor = len(_color)
    for n, _ in enumerate(_color):
        # INTERVALS = int((
        #    int(((_max - _min) / _len_color) * (n+1) + _min) - int(((_max - _min) / _len_color) * n + _min))
        # / 2)
        # if INTERVALS < 1:
        #  INTERVALS = 1
        eq_minmax = (_max - _min) 
        if n + 1 < _len_cor:
            yield {
                'mini': int((eq_minmax / _len_cor) * n + _min),
                'maxi': int((eq_minmax / _len_cor) * (n + 1) + _min),
                'minf': ((eq_minmax / _len_cor) * n + _min) / _convert,
                'maxf': ((eq_minmax / _len_cor) * (n + 1) + _min) / _convert,
                'color0': _color[n],
                'color1': _color[n + 1],
                #'INTERVALS': INTERVALS
            }
        else:
            yield {
                'mini': int((eq_minmax / _len_cor) * n + _min),
                'maxi': int((eq_minmax / _len_cor) * (n + 1) + _min),
                'minf': ((eq_minmax / _len_cor) * n + _min) / _convert,
                'maxf': ((eq_minmax / _len_cor) * (n + 1) + _min)
                / _convert,
                'color0': _color[n - 1],
                'color1': _color[n],
                #'INTERVALS': INTERVALS
            }

def creat_pallet_txt(filename,start, end, p_color):
    _color = [ImageColor.getcolor(cor, "RGB") for cor in p_color]
    _len_cor = len(_color)
    with open(filename, 'w') as file:
        for n, cor in enumerate(_color):
            r,g,b = cor
            eq_minmax = (end - start)
            mini = int((eq_minmax / _len_cor) * n + start)
            maxi = int((eq_minmax / _len_cor) * (n + 1) + start)
            file.write(f'{mini}-{maxi}: {r} {g} {b} 255\n')




def create_folder_for_tiffs(path_level1, name):
    if not isdir(path_level1):
        os.mkdir(path_level1)
    if not isdir(f'{path_level1}/{name}'):
        os.mkdir(f'{path_level1}/{name}')



def creat_titles(dir_file):
    options = {
        'zoom': (5,9),
        'webviewer':'openlayers',
        'resume':False,
        'resampling':'bilinear'
        }
    file = f'{dir_file}_color.tif'
    logger.debug(f'{file}')
    if isfile(file):
        logger.debug('Chamando gdal2title')
        gdal2tiles.generate_tiles(file, dir_file, **options)