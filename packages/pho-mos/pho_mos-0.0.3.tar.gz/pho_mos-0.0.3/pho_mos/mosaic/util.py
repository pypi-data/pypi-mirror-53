import random

import PIL
from PIL import Image
from typing import List, Tuple
from collections import deque

from pho_mos.mosaic.transforms import RGBTransform
from pho_mos.util import get_logger

JPG_IMG_LEN = 3
PNG_IMG_LEN = 4
rgb_transform = RGBTransform()

Image.MAX_IMAGE_PIXELS = None
LOGGER = get_logger("MOSAIC_UTIL")


def add_colour_filter(_filter, image):
    return rgb_transform.mix_with(_filter, factor=.30).applied_to(image)


def get_colour_distance(target_colour, img_colour) -> int:
    """
    Count colour distance between two pixels.
    Манхетонское расстояние между двумя пикселями

    :param target_colour:
    :param img_colour:
    :return:
    """

    def _preprocess_img_len(img):
        if len(img) == JPG_IMG_LEN:
            return [col for col in img]  # + [255]  # jpg has no capacity
        elif len(img) == PNG_IMG_LEN:
            return img
        else:
            raise Exception(
                "Wrong img colour length size: {0}".format(len(img))
            )

    try:
        target_colour = _preprocess_img_len(target_colour)
        img_colour = _preprocess_img_len(img_colour)

        distance = 0
        for ind, colour in enumerate(target_colour):
            distance += abs(colour - img_colour[ind])
        return distance
    except Exception as exception:
        LOGGER.debug("Exception in get_average_colour: {0}".format(exception))


'''
считает средний свет картинки
'''


def get_average_color(image: PIL.Image) -> List[int]:
    """
    Counts average colour of the image.

    :param image: Image
    :return: List[int] size of image channels amount - список из трех цветов по (R,G,B,capacity).
    """
    try:
        pixels = image.load()
        channels_amount = len(pixels[0, 0])
        colours = [0] * channels_amount
        for x in range(image.width):
            for y in range(image.height):
                for channel in range(channels_amount):
                    colours[channel] += pixels[x, y][channel]

        pix_amount = image.width * image.height
        return list(
            map(lambda chanel: int(chanel / pix_amount), colours)
        )
    except Exception as exception:
        LOGGER.debug("Exception in get_average_colour: {0}".format(exception))


'''
возващает наиболее подходящую картинку
'''


def get_next_near_image(target_pixel: Tuple,
                        sorted_source_images: List[any],
                        with_used=True,
                        last_use=False,
                        use_priority=True) -> any:
    """
    Find nearest image from images_pixel with fixed accuracy.
    returns best MosiaicSourceImages

    :param with_used: использовать ли уже отданные картинки (с is_used = True)
    :param last_use: если True, выданная картинка больше не будет ранжироваться в следующих обращениях к get_best_image
    :param target_pixel: Tuple (R,G,B,capacity)
    :param accuracy: int
    :return:
    """
    try:
        min_distance = 1000
        result = sorted_source_images[-1]

        good_results_dequeue: deque = deque(maxlen=3)

        # в этой ссылке лучшая картинка, которая уже использовалась
        # она возвращается, если если все уже использованы
        # best_used_result = sorted_source_images[-1]

        # на сколько может быть больше расстояние между текущим результатом и новым, чтобы приоритет картинки позволил смениьть результат
        # параметр позволяет использовать более приоритетную картику, если она чуть дальше по расстоянию
        replace_distance_delta = 100

        for image in reversed(sorted_source_images):

            if not with_used and image.is_used:
                # пропускаем используемую картинку
                continue

            distance = get_colour_distance(target_pixel, image.image_average_color)
            if use_priority:
                # меняем если больше приоритет или меньше дистанция до точки
                if ((distance <= min_distance and image.priority <= result.priority) or
                        (distance <= min_distance + replace_distance_delta and image.priority < result.priority)):
                    result = image
                    min_distance = distance
                    good_results_dequeue.append(image)
            else:
                if distance <= min_distance:
                    result = image
                    min_distance = distance
                    good_results_dequeue.append(image)

        # если все использованы, а хотели новую, возвращаем использованную
        if len(good_results_dequeue) == 0 and not with_used:
            return get_next_near_image(target_pixel, sorted_source_images, with_used=True, use_priority=use_priority)

        for i in range(0, random.randrange(good_results_dequeue.__len__())):
            result = good_results_dequeue.popleft()

        if last_use:
            # проставляем, что уже использовалась
            result.is_used = True

        return result

    except Exception as exception:
        LOGGER.debug("Exception in get_best_image: {0}".format(exception))


'''
считает максимальную дельту между пикселями из массива и говорит, превышает ли она порог
'''


def check_max_pixel_delta_not_greater_porog(pixel_list: List[Tuple], porog: int) -> bool:
    """
    :param pixel_list: список элементов (R,G,B,capacity)
    :return: максимальное расстояние
    """
    max_distance = 0
    for i1, val1 in enumerate(pixel_list):
        for i2, val2 in enumerate(pixel_list):
            if i1 != i2:
                # LOGGER.debug("Calc colour distance between "+str(val1)+" and "+str(val2))
                delta = get_colour_distance(val1, val2)
                # LOGGER.debug("Colour distance " + str(delta))
                if delta > max_distance:
                    max_distance = delta
                if max_distance > porog:
                    return False

    return True


def calc_gradient_field(target_image: PIL.Image.Image) -> dict:
    """
    считает градиентное поля входного изображения (градиентом в точке называем сумму манхет.расстояний с ее соседями)
    :param target_image:
    :return: словарь. ключ - список [x,y] значение - градиент в точке [x,y]
    """
    target_image_pixels = target_image.load()

    gradient_field_dict = {}

    delta_x_lev = 0
    delta_y_verh = 0

    for x in range(0, target_image.width - 1):
        for y in range(0, target_image.height - 1):

            # LOGGER.debug("Calc gradient for " + str(x)+"x"+str(y))

            if x != target_image.width:
                delta_x_prav = get_colour_distance(target_image_pixels[x + 1, y], target_image_pixels[x, y])
            else:
                delta_x_prav = 0
            if y != target_image.height:
                delta_y_niz = get_colour_distance(target_image_pixels[x, y + 1], target_image_pixels[x, y])
            else:
                delta_y_niz = 0

            gradient_field_dict[(x, y)] = delta_y_niz + delta_x_lev + delta_x_prav + delta_y_verh

            delta_x_lev = delta_x_prav
            delta_y_verh = delta_y_niz

    LOGGER.debug("Gradient field dict: " + str(gradient_field_dict))

    return gradient_field_dict
