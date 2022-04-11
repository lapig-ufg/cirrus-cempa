from pickle import load

from dynaconf import Dynaconf
from loguru import logger
import numpy as np
# import necessary packages
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

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
            'type': np.int16,
            'color': ['#0000ff', '#0021f7', '#005ce6', '#0076dd', '#00b7c4', '#00b38f', '#00aa72', '#00993d', '#008000', '#239c00', '#52b800', '#6ec700', '#d6f100', '#ffdd00', '#ffcc00', '#ffaa00', '#ff7700', '#ff6600', '#ff3300', '#ff0000'],
            'convert': 1000
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
            'type': np.int16,
            'color': ['#0000ff', '#0021f7', '#005ce6', '#0076dd', '#00b7c4', '#00b38f', '#00aa72', '#00993d', '#008000', '#239c00', '#52b800', '#6ec700', '#d6f100', '#ffdd00', '#ffcc00', '#ffaa00', '#ff7700', '#ff6600', '#ff3300', '#ff0000'],
            'convert': 100
            
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
            'type': np.int16,
            'color': ['#ff0000', '#ff2200', '#ff4400', '#ff6600', '#ff8800', '#ffaa00', '#ffcc00', '#ffee00', '#ffff00', '#b0e300', '#6ec700', '#39aa00', '#108e00', '#009127', '#00a256', '#00b38f', '#00b7c4', '#008ed5', '#005ce6', '#0021f7'],
            'convert': 100
        },

        'PRECIP': {
            'layers': [(-1, 'value')],
            'comment': '- RAMS : total accum precip                      [mm liq  ]',
            'type': np.int32,
            'color': ['#ffffff', '#e7e7d7', '#9fdf9f', '#0000ff', '#0000ff', '#005ce6', '#00b7c4', '#00a256', '#00993d', '#008000', '#239c00', '#6ec700', '#8ed500', '#ffff00', '#ffdd00', '#ffaa00', '#ff6600', '#ff2200', '#ff1100', '#ff0000'],
            'convert': 100
        },
        
        'T2MJ': {
            'layers': [(-1, 'value')],
            'comment': '- RAMS : temp - 2m AGL;                          [C       ]',
            'type': np.int16,
            'color': ['#0000ff', '#0021f7', '#005ce6', '#0076dd', '#00b7c4', '#00b38f', '#00aa72', '#00993d', '#008000', '#239c00', '#52b800', '#6ec700', '#d6f100', '#ffdd00', '#ffcc00', '#ffaa00', '#ff7700', '#ff6600', '#ff3300', '#ff0000'],
            'convert': 100
        },
        'TD2MJ': {
            'layers': [(-1, 'value')],
            'comment': '- RAMS : Dewpoint temp in 2m                     [C       ]',
            'type': np.int16,
            'color': ['#0000ff', '#0021f7', '#005ce6', '#0076dd', '#00b7c4', '#00b38f', '#00aa72', '#00993d', '#008000', '#239c00', '#52b800', '#6ec700', '#d6f100', '#ffdd00', '#ffcc00', '#ffaa00', '#ff7700', '#ff6600', '#ff3300', '#ff0000'],
            'convert': 100
        },
        'ALBEDT': {
            'layers': [(-1, 'value')],
            'comment': '- RAMS : albedt                                  [        ]',
            'type': np.int16,
            'color': ['#0000ff', '#0021f7', '#005ce6', '#0076dd', '#00b7c4', '#00b38f', '#00aa72', '#00993d', '#008000', '#239c00', '#52b800', '#6ec700', '#d6f100', '#ffdd00', '#ffcc00', '#ffaa00', '#ff7700', '#ff6600', '#ff3300', '#ff0000'],
            'convert': 1000
        },
    }






def send_email(message):
    # set up the SMTP server
    s = smtplib.SMTP(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT,)
    s.starttls()
    s.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)

    for email in settings.EMAIL_LIST:
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template

        # setup the parameters of the message
        msg['From']=settings.EMAIL_ADDRESS,
        msg['To']=email
        msg['Subject']=f"[logger] {settings.EMAIL_SUBJECT}"

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
        s.send_message(msg)
        
        del msg

