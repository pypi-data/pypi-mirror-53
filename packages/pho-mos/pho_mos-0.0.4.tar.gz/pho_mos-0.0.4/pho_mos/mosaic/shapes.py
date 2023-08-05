

class Point:
    def __init__(self, x: int, y:int):
        self.x = x
        self.y = y

class Rectangle:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # фигуры внутри текущего прямоугольника
        # ключ - Point левого верхего угла, значение - Rectangle
        self.inner_rectangles = {}

        # поле хранящее ссылку на изображение, которому соотвестствиет данный прямоугольник
        self.image: any = None


    def add_inner_rectangle(self, start_point: Point, rectangle):
        self.inner_rectangles[start_point] = rectangle

    # занята ли точка какой-то фигурой
    def is_occupied_point(self, point: Point) -> bool:
        for key_point, value_rect in self.inner_rectangles.items():
            if point.x>=key_point.x and point.x<=key_point.x+value_rect.width-1 \
                    and point.y>=key_point.y and point.y<=key_point.y+value_rect.height-1:
                return True
        return False



