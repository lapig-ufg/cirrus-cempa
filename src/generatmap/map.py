from jinja2 import Environment, PackageLoader, select_autoescape
from sqlalchemy import select

#from cirrus.model import StyleMap
from cirrus.util.config import logger, settings
from cirrus.util.db import create_session
from cirrus.util.functions import get_min_max, get_pallet


def creat_map_file(
    file_name, name, coll_name, min_max, file_date='', geotiff=True
):
    logger.info('ADD no .map para o tiff {file_name}')
    env = Environment(
        loader=PackageLoader('generatmap'), autoescape=select_autoescape()
    )

    with open(f'{settings.CATALOG}{settings.MAPFILE}', 'a') as file_object:
        template = env.get_template('cempa.map')
        row = {}
        logger.info('Gerando .map com dados padrao')
        title = f"{name.lower()} {coll_name.replace('_', ' ').replace('value','')} {file_date}"
        row['view_name'] = title
        row['ows_title'] = title
        row['ows_abstract'] = title
        row['geotiff'] = geotiff
        if geotiff:
            row['coll_view'] = 'pixel'
            row['file_name'] = file_name
        try:
            file_object.write(
                template.render(
                    {
                        **row,
                        'styles': get_pallet(
                            *min_max,
                            name.lower(),
                        ),
                    }
                )
            )
        except:
            logger.exception('Error')


def creat_by_bd():
    env = Environment(
        loader=PackageLoader('generatmap'), autoescape=select_autoescape()
    )

    with open(settings.MAPFILE, 'w') as file_object:
        template = env.get_template('cempa.map')
        session = create_session()
        for row in session.execute(select(StyleMap)).all():
            try:
                row = row[0]
                logger.info(
                    "Creating layer '{}' from variable '{}'".format(
                        row['table_name'], row['coll_table']
                    )
                )
                file_object.write(
                    template.render(
                        {
                            **row.to_dict(),
                            'styles': get_pallet(
                                *get_min_max(row.coll_table, row.table_name),
                                row.palette,
                            ),
                        }
                    )
                )
            except:
                logger.exception('Error')
