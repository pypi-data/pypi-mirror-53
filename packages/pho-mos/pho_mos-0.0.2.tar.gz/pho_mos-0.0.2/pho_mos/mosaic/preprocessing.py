import os
import PIL
from PIL import Image

from pho_mos.util import get_logger

LOGGER = get_logger("MOSAIC")


def open_as_pil_image(filename: str) -> PIL.Image:
    img = None
    try:
        img = Image.open(filename).convert('RGB')
    except Exception as exception:
        LOGGER.error("Error in _open: {0}".format(exception))
        if ".png" in filename:
            filename = filename.replace(".png", ".jpg")
            LOGGER.debug("Renamed: {0}".format(filename))
            img = Image.open(filename).convert('RGB')
    finally:
        # специально, чтобы заранее знать битые файлы
        assert img is not None
        return img


def square_img(image: PIL.Image,
               img_size: int = -1) -> PIL.Image:
    """
    Make image squared.

    :param img_size: размер результата. если не указан, соответствует минимальному габариту исходной
    :param image: Image
    :return: Image
    """
    assert image is not None
    try:
        width, height = image.size
        mean = abs(width - height) / 2.0
        if width > height:
            box = (mean, 0, width - mean, height)
        else:
            box = (0, mean, width, height - mean)
        image = image.crop(box=tuple(map(lambda x: int(x), box)))

        if img_size != -1:
            image = image.resize(size=(
                int(img_size), int(img_size)))

        return image
    except Exception as exception:
        print("Exception in preprocess_img: {0}".format(exception))
        return image


def resize_img(source_path: str,
               target_path: str = None,
               resize_factor: float = 64,
               is_save: bool = True) -> PIL.Image:
    """
    Меняем размер изорбажения в resize_factor раз.

    1. Makes img squared;
    2. Resize image;

    :param source_path: Union[os.path, str] - Path to the source img;
    :param target_path: Optional[Union[os.path, str]] - Path to save preprocessed img;
    :param resize_factor: int - во сколько раз увеличить изображение;
    :param is_return: bool - return result img or not;
    :param is_save: bool - save result img or not;
    :return:
    """
    try:

        image: PIL.Image = open_as_pil_image(source_path)

        if is_save:
            if not target_path:
                target_path = source_path

            if target_path == source_path and ".png" in target_path:
                os.remove(target_path)
                target_path = target_path.replace(".png", ".jpg")
                print(target_path)

        image = image.resize(size=(
            int(image.size[0]*resize_factor), int(image.size[1]*resize_factor))
                             )
        image = image.convert("RGB")
        if is_save:
            image.save(target_path)
        return image

    except Exception as exception:
        LOGGER.error("Exception in preprocess_img: {0}".format(exception))


def to_square_img(source_path: str,
               target_path: str = None,
               img_size: int = 64,
               is_save: bool = True) -> PIL.Image:
    """
    Превращает изображение в квадрат размера img_size

    1. Makes img squared;
    2. Resize image;

    :param source_path: Union[os.path, str] - Path to the source img;
    :param target_path: Optional[Union[os.path, str]] - Path to save preprocessed img;
    :param img_size: int - во сколько раз увеличить изображение;
    :param is_return: bool - return result img or not;
    :param is_save: bool - save result img or not;
    :return:
    """
    try:

        image: PIL.Image = open_as_pil_image(source_path)

        if is_save:
            if not target_path:
                target_path = source_path

            if target_path == source_path and ".png" in target_path:
                os.remove(target_path)
                target_path = target_path.replace(".png", ".jpg")
                print(target_path)

        image = square_img(image)
        image = image.resize(size=(img_size, img_size))
        if is_save:
            image.save(target_path)
        return image

    except Exception as exception:
        LOGGER.error("Exception in preprocess_img: {0}".format(exception))

'''
возвращает лист со строительными картинками нужного размера
'''
def batch_preprocess(source_dirname: str,
                     target_dirname: str = None,
                     img_size: int = 64,
                     is_save=True) -> list:
    """
    Image preprocessing by batch.

    Resize image;

    :param source_dirname: - source photos dir name;
    :param target_dirname: - target dir name to save photos;
    :param img_size: int - preprocessed img size;
    :param is_save: bool - save result imgs or not;
    :return: list of PIL.Image
    """
    try:
        print(source_dirname)

        if not os.path.exists(source_dirname):
            print("Warning: No such directory {0}".format(source_dirname))
            return

        if is_save:
            if not target_dirname:
                target_dirname = source_dirname
            else:
                if not os.path.exists(target_dirname):
                    os.mkdir(target_dirname)
        imgs = []

        for name in os.listdir(source_dirname):
            path = os.path.join(source_dirname, name)
            if is_save:
                targer_path = os.path.join(target_dirname, name)
            else:
                targer_path = ""
            img = to_square_img(path, targer_path, img_size, is_save=is_save)
            imgs.append(img)

        LOGGER.debug("Source images: "+str(imgs))

        return imgs

    except Exception as exception:
        LOGGER.error("Exception in batch_preprocess: {0}".format(exception))