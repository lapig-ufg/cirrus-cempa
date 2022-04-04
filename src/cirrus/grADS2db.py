import numpy as np
from cirrus.grADS2tif import grADS2tiff
import rioxarray
from xgrads import open_CtlDataset
import pandas as pd
from multiprocessing import Pool
from glob import glob


from cirrus.util.config import variables, settings, logger
#from cirrus.util.db import save_df_bd


def get_time(dataframe):
    return pd.to_datetime(dataframe.time.data[0])


def grads_to_sql(file_name):
    dfs = {}
    logger.info(file_name)
    with open_CtlDataset(file_name) as file:
        dataframe = file
        for name in variables:
            logger.debug(f'{file_name} {name}')

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
                    grADS2tiff(dataframe, name, layer_name,_id)
                    layers[layer_name] = np.meshgrid(var[_id], indexing='ij')[
                        0
                    ]
                else:
                    grADS2tiff(dataframe, name, layer_name)
                    layers[layer_name] = np.meshgrid(var, indexing='ij')[0]

            temp_df = pd.DataFrame(
                {'datetime': vtime, **layers, 'point_gid': gid}
            )
            #save_df_bd(temp_df, name.lower())
            _min = temp_df.min()
            _max = temp_df.max()
            dfs[name] = pd.concat(
                [
                    pd.DataFrame(_max).T.drop(columns='point_gid'),
                    pd.DataFrame(_min).T.drop(columns='point_gid'),
                ]
            )
    return dfs

def to_db():
    with Pool(settings.N_POOL) as workers:
        returns = workers.map(grads_to_sql, glob(f'{settings.CEMPADIR}downloads/*.ctl')[:5])


    tmp_max_minx = {}
    for result in returns:
        for i in result:
            try:
                tmp_max_minx[i] = pd.concat([tmp_max_minx[i], result[i]])
            except Exception as e:
                tmp_max_minx[i] = result[i]


    max_minx = {}
    for name in tmp_max_minx:
        max_minx[name] = {
            'max': tmp_max_minx[name].resample('D', on='datetime').max(),
            'min': tmp_max_minx[name].resample('D', on='datetime').min(),
        }
    print(max_minx)

    ## Creat .map

    tifs_path = f'{settings.CATALOG}cempa_tifs'

    files = glob(f'{tifs_path}/*/*/*.tif')
    print(files)
    import ipdb; ipdb.set_trace()


if __name__ == '__main__':
    to_db()