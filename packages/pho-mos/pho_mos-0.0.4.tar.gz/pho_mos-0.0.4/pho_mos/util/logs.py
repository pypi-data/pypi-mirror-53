import os

THIS_FILE_PATH = os.path.dirname(os.path.abspath(__file__))

import logging

main_component = "THEME_MOSAIC"
logging.basicConfig(
    format='%(levelname)s: [%(asctime)s.%(msecs)03d] {} %(name)s '
           '%(filename)s:%(funcName)s:%(lineno)s:  %(message)s'.format(main_component),
    datefmt='%Y-%m-%d %H:%M:%S', level='DEBUG')


def get_logger(TAG: str='') -> logging.Logger:
    return logging.getLogger(TAG)

# info - измениние состояния компанента системы
# debug - все потоковые события
# warning - обработанные ошибки (переподключение)
# error - Exceptions
# critical - не загрузились модули
