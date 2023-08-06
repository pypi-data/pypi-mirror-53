import logging


def set_config(**kwargs):
    """
    :param kwargs:
    :return:
    """
    log_level = logging.DEBUG
    log_filename = kwargs.get('logging_filename', None)
    log_format = '%(asctime)-15s %(levelname)s [%(name)s] [in %(pathname)-10s:%(funcName)-20s:%(lineno)-5d]: ' \
                 '%(message)s'
    logging.basicConfig(
        format=log_format,
        filename=log_filename,
        level=log_level,
        filemode='w',
    )


set_config()
