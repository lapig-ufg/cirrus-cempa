import os
from datetime import datetime
from glob import glob
from os.path import isdir
import seaborn as sns
from matplotlib import pyplot as plt

from cirrus.util.color import color
from cirrus.util.config import logger, variables
from cirrus.util.db import create_session



def colobar_convert(n,start,end,_len_color):
  return f'{((end - start) / _len_color) * n + start:.1f}'


def view_colormap(fname, cmap,start, end):
    """Plot a colormap with its grayscale equivalent"""
    plt.rc('xtick', labelsize=16)  
    cmap = sns.color_palette(cmap)
    colors = cmap
    
    fig, ax = plt.subplots(1, figsize=(10, 1),
                           subplot_kw=dict(xticks=[], yticks=[]))
    plt.xticks(range(0,21,2),[colobar_convert(n,start,end,20) for n in range(0,21,2)]) 
    ax.imshow([colors], extent=[0,20, 0, 1])
    plt.savefig(fname,dpi=300, transparent=False)

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
    _len_color = len(_color)

    yield from [
        {
            'mini': int(((_max - _min) / _len_color) * n + _min),
            'maxi': int(((_max - _min) / _len_color) * (n+1) + _min),

            'minf': (((_max - _min) / _len_color) * n + _min)/_convert,
            'maxf': (((_max - _min) / _len_color) * (n+1) + _min)/_convert,
            'color': color,
        }
        for n, color in enumerate(
            _color
        )
    ]


def create_folder_for_tiffs(path_level1, name):
    if not isdir(path_level1):
        os.mkdir(path_level1)
    if not isdir(f'{path_level1}/{name}'):
        os.mkdir(f'{path_level1}/{name}')
