from datetime import datetime
from glob import glob
from multiprocessing import Pool, cpu_count
from os import remove
from os.path import isfile
import subprocess
import numpy as np
import pandas as pd
import rioxarray
from xgrads import open_CtlDataset

from cirrus.grADS2tif import grADS2tiff
from cirrus.util.config import logger, settings, variables
from cirrus.util.db import save_df_bd
from cirrus.util.functions import creat_pallet_txt, view_colormap
from generatmap.map import creat_map_file


def get_time(dataframe):
    return pd.to_datetime(dataframe.time.data[0])


def grads_to_sql(file_name):
    dfs = {}
    logger.info(file_name)
    _start = datetime.now()
    with open_CtlDataset(file_name) as file:
        dataframe = file
        for name in variables:
            logger.info(f'{file_name} {name}')

            var = dataframe.variables[name][0]
            vtime, *_ = [
                x.flatten()
                for x in np.meshgrid(
                    get_time(dataframe),
                    dataframe.lat,
                    dataframe.lon,
                    indexing='ij',
                )
            ]
            layers = {}
            gid = [i for i, _ in enumerate(vtime, 1)]
            for _id, layer_name in variables[name]['layers']:
                if _id > -1:
                    grADS2tiff(dataframe, name, layer_name, _id)
                    layers[layer_name] = np.meshgrid(var[_id], indexing='ij')[
                        0
                    ]
                else:
                    grADS2tiff(dataframe, name, layer_name)
                    layers[layer_name] = np.meshgrid(var, indexing='ij')[0]
            logger.info(f'tifs criados {name}')
            temp_df = pd.DataFrame(
                {'datetime': vtime, **layers, 'point_gid': gid}
            )
            # Salvar no banco de dados
            save_df_bd(temp_df, name.lower(),file_name)
            _min = temp_df.min()
            _max = temp_df.max()
            dfs[name] = pd.concat(
                [
                    pd.DataFrame(_max).T.drop(columns='point_gid'),
                    pd.DataFrame(_min).T.drop(columns='point_gid'),
                ]
            )
    logger.info(f'{file_name} Time: {datetime.now() - _start}')
    return dfs



def creat_map_and_bar(args):
    file, max_minx = args
    day = file.split('/')[-3].split('T')[0]
    var = file.split('/')[-2].upper()
    layer = file.split('/')[-1].replace('.tif', '')
    dfmax = max_minx[var]['max']
    dfmin = max_minx[var]['min']
    _max = float(dfmax[dfmax.index == day][layer])
    _min = float(dfmin[dfmin.index == day][layer])
    _convert = variables[var]['convert']
    
    title = (
        f"{var.lower()}_{layer.replace('value','')}_{file.split('/')[-3]}"
    )
    color_bar = f'{settings.CATALOG}colorbar'
    color_txt = f'{color_bar}/{title}.txt'
    view_colormap(f'{color_bar}/{title}.png', variables[var]['color'], _min, _max)
    creat_pallet_txt(color_txt, int(_min * _convert), int(_max * _convert), variables[var]['color'])
    cmd = f'gdaldem color-relief {file} {color_txt} {file.replace(".tif","_color.tif")}'

    logger.info('Create imagecolor {file}')
    logger.debug(cmd)
    subprocess.call(cmd.split())
    return (creat_map_file(
        file,
        var,
        layer,
        (int(_min * _convert), int((_max + 0.01) * _convert)),
        file.split('/')[-3],
    ), title)






def to_db():
    logger.info('Montado as Pool')
    with Pool(settings.N_POOL) as workers:
        returns = workers.map(
            grads_to_sql, glob(f'{settings.CEMPADIR}downloads/*.ctl')
        )

    tmp_max_minx = {}
    for result in returns:
        for i in result:
            try:
                tmp_max_minx[i] = pd.concat([tmp_max_minx[i], result[i]])
            except Exception as e:
                tmp_max_minx[i] = result[i]

    max_minx = {}
    meta_path = f'{settings.CATALOG}cempa_metadata'
    for name in tmp_max_minx:
        __max = tmp_max_minx[name].resample('D', on='datetime').max()
        __min = tmp_max_minx[name].resample('D', on='datetime').min()
        __max.to_csv(f'{meta_path}/{name}_max.csv')
        __min.to_csv(f'{meta_path}/{name}_min.csv')
        max_minx[name] = {
            'max': __max,
            'min': __min,
        }
    tifs_path = f'{settings.CATALOG}cempa_tifs'

    ## Creat .map
    tifs_path = f'{settings.CATALOG}cempa_tifs'
    
    files = glob(f'{tifs_path}/*/*/*.tif')
    if isfile(f'{settings.CATALOG}{settings.MAPFILE}'):
        remove(f'{settings.CATALOG}{settings.MAPFILE}')
    # TODO fazer com multiprocess
    args_to_map_and_bar = [(file, max_minx) for file in files]

    with Pool(int(cpu_count()-2)) as workers:
        returns_map_and_bar = workers.map(
            creat_map_and_bar, args_to_map_and_bar
        )

    biglayer = []
    text_list = []
    logger.debug('join no .map e append nos title')
    for tmp_text, title in returns_map_and_bar:
        text_list.append(tmp_text)
        biglayer.append(title)
    text = '\n'.join(text_list)

    with open(f'{settings.CATALOG}{settings.MAPFILE}', 'w') as file_object:
        file_object.write(text)
    logger.debug('.map criado')
    return sorted(biglayer)


if __name__ == '__main__':
    to_db()
