from jinja2 import Environment, PackageLoader, select_autoescape
from sqlalchemy import select

# from cirrus.model import StyleMap
from cirrus.util.config import logger, settings
from cirrus.util.db import create_session
from cirrus.util.functions import get_min_max, get_pallet


def creat_map_file(
    file_name, name, coll_name, min_max, file_date='', geotiff=True
):

    env = Environment(
        loader=PackageLoader('generatmap'), autoescape=select_autoescape()
    )

    
    template = env.get_template('cempa.map')
    template_color = env.get_template('cempa_color.map')
    row = {}

    logger.info(f'ADD no .map para o tiff {file_name}')
    title = f"{name.lower()}_{coll_name.replace('value','')}_{file_date}"
    row['view_name'] = title
    row['ows_title'] = title
    row['ows_abstract'] = title
    row['geotiff'] = geotiff
    if geotiff:
        row['coll_view'] = 'pixel'
        row['file_name'] = file_name
    try:
        raw_map = template.render(
            {
                **row,
                'styles': get_pallet(
                    *min_max,
                    name,
                ),
             }
        )
        row['file_name'] = file_name.replace('.tif','_tiled.tif')
        color_map =template_color.render(
            row
        )


        return  f'{raw_map}\n{color_map}'
    
    except:
        logger.exception('Error')
        return ''


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
