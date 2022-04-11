root = '/STORAGE/catalog/cempa_tifs/2022-04-06T14-00/albedt'

import rasterio

from cirrus.util.config import logger
with rasterio.open(f'{root}/value.tif') as src:
        shade = src.read(1)
        meta = src.meta

with rasterio.open(f'{root}/color_value.tif', 'w', **meta) as dst:
    dst.write(shade, indexes=1)
    dst.write_colormap(
            1, {
                0: (255, 0, 0, 255),
                255: (0, 0, 255, 255) })



logger.error('teste')