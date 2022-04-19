import asyncio
import json
import math
from multiprocessing import Pool
from pickle import load

import aiohttp

from cirrus.util.config import logger, settings

BBOX_BRAZIL = {
    'bottom': -21.0000000000000000,
    'left': -55.0000000000000000,
    'top': -8.9754829406738299,
    'right': -42.9614372253417969,
}

meta_path = f'{settings.CATALOG}cempa_metadata'


MAX_ZOOM_LEVEL = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
# PORT 5000 - HOMOLOGAÇÃO
# PORT 3000 - PRODUÇÃO
OWS_URL = settings.OWS_ROOT_URL


urls = []


def lonToX(lon, zoom):
    n = math.pow(2, zoom)
    x = math.floor((lon + 180) / 360 * n)
    return x


def latToY(lat, zoom):
    lat_rad = lat * math.pi / 180
    n = math.pow(2, zoom)
    y = math.floor(
        (1 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi)
        / 2
        * n
    )
    return y


def tilesInBbox(bbox, zoom):
    tiles = []
    xMin = lonToX(bbox['left'], zoom)
    xMax = lonToX(bbox['right'], zoom)
    yMin = latToY(bbox['top'], zoom)
    yMax = latToY(bbox['bottom'], zoom)

    x = xMin
    while x <= xMax:
        y = yMin
        while y <= yMax:
            tiles.append((x, y, zoom))
            y = y + 1
        x = x + 1

    return tiles


def general(layer):
    for zoom in MAX_ZOOM_LEVEL:
        tiles = tilesInBbox(BBOX_BRAZIL, zoom)
        for x, y, z in tiles:
            # % (OWS_URL, layer, year, , , tile['z']
            yield f'{OWS_URL}?layers={layer}&mode=tile&tile={x}+{y}+{z}&tilemode=gmap&map.imagetype=png'


async def processRequests(layer):
    async with aiohttp.ClientSession() as session:
        for url in general(layer):
            async with session.get(url) as resp:
                status = resp.status
                txt = await resp.read()
                del txt
                logger.debug(url, status)


def load_layer(layer):
    asyncio.run(processRequests(layer))


def run(LAYERS):
    with Pool(settings.N_POOL) as workes:
        result = workes.map(load_layer, LAYERS)
