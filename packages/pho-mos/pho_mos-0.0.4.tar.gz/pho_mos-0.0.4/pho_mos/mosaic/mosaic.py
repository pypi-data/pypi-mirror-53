import os
import traceback
from typing import List, Tuple

import PIL
from PIL import Image

from pho_mos.mosaic.shapes import Rectangle, Point
from pho_mos.mosaic.util import get_average_color, get_next_near_image, add_colour_filter, \
    calc_gradient_field
from .preprocessing import resize_img, open_as_pil_image, square_img

from pho_mos.util.logs import get_logger

Image.MAX_IMAGE_PIXELS = None
LOGGER = get_logger("MOSAIC")


class MosiaicSourceImage:

    def __init__(self, path, cell_size: int, priority: int = 1):
        # перегоняем в PIL, заготавливаем маленький квадрат, считаем средний цвет
        self.origin_img: PIL.Image = open_as_pil_image(path)
        self.squared_image: PIL.Image = square_img(self.origin_img, cell_size)
        self.image_average_color = get_average_color(self.squared_image)

        self.priority = priority
        self.is_used = False

# для сортировки в списке
def get_mosaic_image_priority(image: MosiaicSourceImage):
    return image.priority

'''
рисует мозайку попиксельно заменяя на картинку
'''
def build_mosaic(target_image: PIL.Image.Image,
                 source_images: List[MosiaicSourceImage],
                 ukrup_field_max_percent: float = 0.1,
                 cell_size: int = 64,
                 not_ukrup_fields: List[Tuple] = []
                 ) -> PIL.Image.Image:
    """
    Build mosaic from target_image and list of source_images.

    NOTE:
        build картинки дб приведены к квадрату ребром img_size;

    :param not_ukrup_fields:
    :param ukrup_field_max_percent:
    :param target_image: Image
    :param source_images: List[str] - список к путями к изображениям - кирпичам
    :param random_param: randomization parameter to choose best image for pixel;
    :param cell_size: размер сетки - минимальный размер картинки
    :return:
    """
    try:
        LOGGER.debug("BUILD START. target_image: " + str(target_image.width)+"x"+str(target_image.height))
        LOGGER.debug("BUILD START. building_images: " + str(source_images))
        target_image_pixels = target_image.load()

        # сортируем картинки по приоритету
        source_images.sort(key=get_mosaic_image_priority)
        # TODO избавиться от этого:
        source_image_average_colors = {}
        for index, img in enumerate(source_images):
            source_image_average_colors[index] = img.image_average_color

        output_dims = (
            target_image.width * cell_size,
            target_image.height * cell_size
        )

        output_image = Image.new("RGB", output_dims)
        # область, хранящая прямоугольники укрупнения
        output_rectangle: Rectangle = Rectangle(target_image.width, target_image.height)
        LOGGER.debug("Created new output image " + str(output_image.width)+"x"+str(output_image.height))

        # словарь с полем градиентов в точках
        target_image_gradient_field_dict = calc_gradient_field(target_image)

        # прямоугольник, содержащий прямоугольники, соответствующие зонам, которые не нужно укрупнять
        not_ukr_fields_rectangle: Rectangle = Rectangle(target_image.width, target_image.height)
        for field in not_ukrup_fields:
            start_point: Point = Point(field[0]*target_image.width, field[1]*target_image.height)
            rectangle: Rectangle = Rectangle((field[2]-field[0])*target_image.width,
                                             (field[3]-field[1])*target_image.height)
            not_ukr_fields_rectangle.add_inner_rectangle(start_point, rectangle)

        # минимальный и максимальный размер области укрупнения
        ukrup_field_max_size: int = int(min(target_image.width, target_image.height) * ukrup_field_max_percent)
        LOGGER.debug("Max ukrup field size "+str(ukrup_field_max_size))

        max_gradient_porog = 120

        LOGGER.debug("RENDER START")

        # заполняем output_rectangle
        # сквозной проход квадратами от размеров ukrup_field_max_size до >3 (выведено эмпирически)
        step = ukrup_field_max_size
        shape_sizes = []

        while step > 3:
            shape_sizes.append(step)
            step = int(step*0.8)

        for size in shape_sizes:

            LOGGER.debug("*** Check size "+str(size))
            x_start_shape = 0

            # цикл по всем возможным точкам начала фигуры
            while x_start_shape <= target_image.width-size:
                y_start_shape = 0
                while y_start_shape <= target_image.height-size:

                    # собираем список градиентов текущего квадрата
                    is_empty_rect_field = True
                    is_consist_greater_porog_gradient_point = False

                    for i in range(0, size-1):
                        # если внутри квадрата уже ловили занятую точку, заканчиваес цикл в холостую
                        if not is_empty_rect_field:
                            break

                        for j in range(0, size-1):
                            # если внутри квадрата уже ловили занятую точку, заканчиваес цикл в холостую
                            if not is_empty_rect_field:
                                break

                            # если точка внутри квадрата занята, пропускаем квадрат
                            if (output_rectangle.is_occupied_point(point=Point(x_start_shape+i, y_start_shape+j)) or
                                not_ukr_fields_rectangle.is_occupied_point(point=Point(x_start_shape+i, y_start_shape+j))):
                                is_empty_rect_field = False
                                break

                            # проверяем, содержит ли область точку с большим градиентом
                            if target_image_gradient_field_dict[(x_start_shape+i, y_start_shape+j)]>max_gradient_porog:
                                is_consist_greater_porog_gradient_point = True


                    # если внутри квадрата уже ловили занятую точку, пропускаем ход и идем к след.квадрату
                    if not is_empty_rect_field:
                        # LOGGER.debug("Field not empty")
                        y_start_shape = y_start_shape + int(size/4)
                        continue

                    # если в области нет точки с высоким градиентом, заполняем изображением size
                    if not is_consist_greater_porog_gradient_point:

                        # заполнение укрупненной области фигурой размера size
                        new_rectangle: Rectangle = Rectangle(size, size)
                        # достаем наиболее подходящую картинку (пока по центральному пикселю)
                        best_img: MosiaicSourceImage  = get_next_near_image(
                            target_image_pixels[int(x_start_shape+size/2), int(y_start_shape+size/2)],
                            source_images,
                            with_used=False,
                            last_use=True,
                            use_priority=True
                        )
                        if best_img is None:
                            raise Exception("Not found best image!")

                        new_rectangle.image = add_colour_filter(target_image_pixels[x_start_shape, y_start_shape],
                                                                best_img.origin_img)
                        new_rectangle.image = square_img(new_rectangle.image, size * cell_size)

                        output_rectangle.add_inner_rectangle(Point(x_start_shape, y_start_shape), new_rectangle)

                        LOGGER.debug("Draw rectangle " + str(x_start_shape) + ":" + str(y_start_shape) + " " + str(new_rectangle.image))
                        output_image.paste(new_rectangle.image, (x_start_shape * cell_size, y_start_shape * cell_size))

                        # если квадрат добавлен, двигаемся сразу к след.точке
                        y_start_shape = y_start_shape + int(size)
                    else:
                        # LOGGER.debug("More than porog")
                        y_start_shape = y_start_shape + int(size/4)

                # по оси абцисс двигаемся скольжением по size / 2
                x_start_shape = x_start_shape + int(size/4)


        #  заполняем все незаполненные поля фигурами размера size
        for x in range(0, target_image.width):
            for y in range(0, target_image.height):
                # если точка занята, не трогаем
                if output_rectangle.is_occupied_point(point=Point(x, y)):
                    continue

                best_img: MosiaicSourceImage = get_next_near_image(
                    target_image_pixels[x, y],
                    source_images,
                    with_used=True,
                    use_priority=False
                )
                img = add_colour_filter(target_image_pixels[x, y],
                                        best_img.squared_image)
                output_image.paste(
                    img, (x * cell_size, y * cell_size)
                )


        LOGGER.debug("BUILD END")

        return output_image

    except Exception as exception:
        LOGGER.debug("Exception in build_mosaic: {0}".format(str(traceback.format_exc())))



'''
создаем мозайку с укрупнением
'''
def create_mosaic(img_path: str,
                  source_dirs: List[str],
                  target_path: str,
                  cell_size: int = 64,
                  resize_factor: float = 0.1,
                  ukrup_field_max_percent: float = 0.1,
                  not_ukrup_fields: List[Tuple] = []
                  ) -> None:
    """
    создать укрупненную мозайку

    :param img_path:
    :param source_dirs: список директорий, из которых брать элементы, в порядке приоритета!
    :param target_path:
    :param cell_size: - размер ячейки, на которые производится разбиение
    :param resize_factor: - во сколько раз увеличится изображение (для больших фото уменьшаем)
    :param ukrup_field_min_percent - минимальный размер области которую можно укрупнить
    :param not_ukrup_fields -  список областей, в которых не требуется укрупнение. область в формате процентов от x,y..
    :return:
    """
    try:

        LOGGER.debug("IN create_mosaic: INSIDE")

        # сделали resize
        target_image: PIL.Image = resize_img(
            img_path,
            resize_factor=resize_factor,
            is_save=False
        )

        if target_image is None:
            LOGGER.error("Cannot open target image! Check path!!!")
            raise Exception("No image under path {0} ".format(img_path))

        LOGGER.debug("IN create_mosaic: PROCESS TARGET")

        # достаем картинки, из которых строится изображение и режем до квадратных
        source_images: List[MosiaicSourceImage] = []
        for index, source_dir in enumerate(source_dirs):
            for name in os.listdir(source_dir):
                path = os.path.join(source_dir, name)
                LOGGER.debug("Append source image: "+path+"; priority "+str(index))
                img: MosiaicSourceImage = MosiaicSourceImage(path, cell_size, priority=index)
                source_images.append(img)

        LOGGER.debug("IN create_mosaic: PROCESS build_batch_images {0}".format(source_images))
        LOGGER.debug("IN create_mosaic: START BUILD")

        image = build_mosaic(target_image, source_images,
                             ukrup_field_max_percent = ukrup_field_max_percent,
                             cell_size= cell_size, not_ukrup_fields = not_ukrup_fields)
        if image is not None:
            image.save(target_path)

    except Exception as e:
        LOGGER.debug("Exception in create_mosaic: {0}".format(traceback.format_exc()))
