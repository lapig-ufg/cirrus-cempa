from pickle import load

from dynaconf import Dynaconf
from loguru import logger
from pandas import read_csv

logger.add(
    '../sys.log',
    format='[{time} | {process.id} | {level: <8}] {module}.{function}:{line} {message}',
    rotation='500 MB',
)

logger.add(
    '../syserror.log',
    format='[{time} | {process.id} | {level: <8}] {module}.{function}:{line} {message}',
    rotation='500 MB',
    level='WARNING',
)


settings = Dynaconf(
    envvar_prefix='CEMPA',
    settings_files=['settings.toml', '.secrets.toml'],
)


with open('./metadata/lonlat.obj', 'rb') as tfile:
    lons, lats = load(tfile)


variables_not_run = {
        'SMOIST1': {
            'layers': [
                (12, 'lev_700'),
                (13, 'lev_750'),
                (14, 'lev_800'),
                (15, 'lev_850'),
                (16, 'lev_900'),
                (17, 'lev_925'),
                (18, 'lev_1000'),
            ],
            'comment': '- RAMS : soil moisture: patch # 1                [m3/m3   ]',
        },
        'SMOIST2': {
            'layers': [
                (12, 'lev_700'),
                (13, 'lev_750'),
                (14, 'lev_800'),
                (15, 'lev_850'),
                (16, 'lev_900'),
                (17, 'lev_925'),
                (18, 'lev_1000'),
            ],
            'comment': '- RAMS : soil moisture: patch # 2                [m3/m3   ]',
        },
        'SMOIST3': {
            'layers': [
                (12, 'lev_700'),
                (13, 'lev_750'),
                (14, 'lev_800'),
                (15, 'lev_850'),
                (16, 'lev_900'),
                (17, 'lev_925'),
                (18, 'lev_1000'),
            ],
            'comment': '- RAMS : soil moisture: patch # 3                [m3/m3   ]',
        },
        'SMOIST4': {
            'layers': [
                (12, 'lev_700'),
                (13, 'lev_750'),
                (14, 'lev_800'),
                (15, 'lev_850'),
                (16, 'lev_900'),
                (17, 'lev_925'),
                (18, 'lev_1000'),
            ],
            'comment': '- RAMS : soil moisture: patch # 4                [m3/m3   ]',
        },
         'UE_AVG': {
            'layers': [
                (0, 'lev_100'),
                (1, 'lev_150'),
                (2, 'lev_200'),
                (3, 'lev_250'),
                (4, 'lev_300'),
                (5, 'lev_350'),
                (6, 'lev_400'),
                (7, 'lev_450'),
                (8, 'lev_500'),
                (9, 'lev_550'),
                (10, 'lev_600'),
                (11, 'lev_650'),
                (12, 'lev_700'),
                (13, 'lev_750'),
                (14, 'lev_800'),
                (15, 'lev_850'),
                (16, 'lev_900'),
                (17, 'lev_925'),
                (18, 'lev_1000'),
            ],
            'comment': '- RAMS : ue_avg                                  [m/s     ]',
        },
        'VE_AVG': {
            'layers': [
                (0, 'lev_100'),
                (1, 'lev_150'),
                (2, 'lev_200'),
                (3, 'lev_250'),
                (4, 'lev_300'),
                (5, 'lev_350'),
                (6, 'lev_400'),
                (7, 'lev_450'),
                (8, 'lev_500'),
                (9, 'lev_550'),
                (10, 'lev_600'),
                (11, 'lev_650'),
                (12, 'lev_700'),
                (13, 'lev_750'),
                (14, 'lev_800'),
                (15, 'lev_850'),
                (16, 'lev_900'),
                (17, 'lev_925'),
                (18, 'lev_1000'),
            ],
            'comment': '- RAMS : ve_avg                                  [m/s     ]',
        },
        'W': {
            'layers': [
                (0, 'lev_100'),
                (1, 'lev_150'),
                (2, 'lev_200'),
                (3, 'lev_250'),
                (4, 'lev_300'),
                (5, 'lev_350'),
                (6, 'lev_400'),
                (7, 'lev_450'),
                (8, 'lev_500'),
                (9, 'lev_550'),
                (10, 'lev_600'),
                (11, 'lev_650'),
                (12, 'lev_700'),
                (13, 'lev_750'),
                (14, 'lev_800'),
                (15, 'lev_850'),
                (16, 'lev_900'),
                (17, 'lev_925'),
                (18, 'lev_1000'),
            ],
            'comment': '- RAMS : w                                       [m/s     ]',
        },
         'GEO': {
            'layers': [
                (0, 'lev_100'),
                (1, 'lev_150'),
                (2, 'lev_200'),
                (3, 'lev_250'),
                (4, 'lev_300'),
                (5, 'lev_350'),
                (6, 'lev_400'),
                (7, 'lev_450'),
                (8, 'lev_500'),
                (9, 'lev_550'),
                (10, 'lev_600'),
                (11, 'lev_650'),
                (12, 'lev_700'),
                (13, 'lev_750'),
                (14, 'lev_800'),
                (15, 'lev_850'),
                (16, 'lev_900'),
                (17, 'lev_925'),
                (18, 'lev_1000'),
            ],
            'comment': '- RAMS : geopotential height                     [m       ]',
        },
        'ACCCON': {
            'layers': [(-1, 'value')],
            'comment': '- RAMS : accum convective pcp                    [mm      ]',
        },
        'SFC_PRESS': {
            'layers': [(-1, 'value')],
            'comment': '- RAMS : Surface pressure                        [mb      ]',
        },
        'SEA_PRESS': {
            'layers': [(-1, 'value')],
            'comment': '- RAMS : sea level pressure;                     [mb;     ]',
        },
        'U10MJ': {
            'layers': [(-1, 'value')],
            'comment': '- RAMS : Zonal Wind at 10m - from JULES          [m/s     ]',
        },
        'V10MJ': {
            'layers': [(-1, 'value')],
            'comment': '- RAMS : Meridional Wind at 10m - from JULES     [m/s     ]',
        },
        'LE': {
            'layers': [(-1, 'value')],
            'comment': '- RAMS : sfc lat heat flx                        [W/m2    ]',
        },
        'H': {
            'layers': [(-1, 'value')],
            'comment': '- RAMS : sfc sens heat flx                       [W/m2    ]',
        },
        'RSHORT': {
            'layers': [(-1, 'value')],
            'comment': '- RAMS : rshort                                  [W/m2    ]',
        },
        'RLONG': {
            'layers': [(-1, 'value')],
            'comment': '- RAMS : rlong                                   [W/m2    ]',
        },
        'RLONGUP': {
            'layers': [(-1, 'value')],
            'comment': '- RAMS : rlongup                                 [W/m2    ]',
        },
    }
variables = {
        'TEMPC': {
            'layers': [
                (0, 'lev_100'),
                (1, 'lev_150'),
                (2, 'lev_200'),
                (3, 'lev_250'),
                (4, 'lev_300'),
                (5, 'lev_350'),
                (6, 'lev_400'),
                (7, 'lev_450'),
                (8, 'lev_500'),
                (9, 'lev_550'),
                (10, 'lev_600'),
                (11, 'lev_650'),
                (12, 'lev_700'),
                (13, 'lev_750'),
                (14, 'lev_800'),
                (15, 'lev_850'),
                (16, 'lev_900'),
                (17, 'lev_925'),
                (18, 'lev_1000'),
            ],
            'comment': '- RAMS : temperature                             [C       ]',
        },
       
        'RH': {
            'layers': [
                (0, 'lev_100'),
                (1, 'lev_150'),
                (2, 'lev_200'),
                (3, 'lev_250'),
                (4, 'lev_300'),
                (5, 'lev_350'),
                (6, 'lev_400'),
                (7, 'lev_450'),
                (8, 'lev_500'),
                (9, 'lev_550'),
                (10, 'lev_600'),
                (11, 'lev_650'),
                (12, 'lev_700'),
                (13, 'lev_750'),
                (14, 'lev_800'),
                (15, 'lev_850'),
                (16, 'lev_900'),
                (17, 'lev_925'),
                (18, 'lev_1000'),
            ],
            'comment': '- RAMS : relative humidity                       [pct     ]',
        },
       
        'CLOUD': {
            'layers': [
                (0, 'lev_100'),
                (1, 'lev_150'),
                (2, 'lev_200'),
                (3, 'lev_250'),
                (4, 'lev_300'),
                (5, 'lev_350'),
                (6, 'lev_400'),
                (7, 'lev_450'),
                (8, 'lev_500'),
                (9, 'lev_550'),
                (10, 'lev_600'),
                (11, 'lev_650'),
                (12, 'lev_700'),
                (13, 'lev_750'),
                (14, 'lev_800'),
                (15, 'lev_850'),
                (16, 'lev_900'),
                (17, 'lev_925'),
                (18, 'lev_1000'),
            ],
            'comment': '- RAMS : cloud mix ratio                         [g/kg    ]',
        },
        'PRECIP': {
            'layers': [(-1, 'value')],
            'comment': '- RAMS : total accum precip                      [mm liq  ]',
        },
        
        'T2MJ': {
            'layers': [(-1, 'value')],
            'comment': '- RAMS : temp - 2m AGL;                          [C       ]',
        },
        'TD2MJ': {
            'layers': [(-1, 'value')],
            'comment': '- RAMS : Dewpoint temp in 2m                     [C       ]',
        },
        'ALBEDT': {
            'layers': [(-1, 'value')],
            'comment': '- RAMS : albedt                                  [        ]',
        },
    }

