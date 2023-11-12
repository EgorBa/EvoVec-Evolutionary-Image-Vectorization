import numpy as np
from PIL import Image
import cv2
from typing import List, Sequence

from dto.area import Area
from dto.svg_segment import M, C, Segment


def read_picture(path: str) -> np.array:
    image = Image.open(path)
    image = image.convert("RGBA")
    new_image = Image.new("RGBA", image.size, "WHITE")  # Create a white rgba background
    new_image.paste(image, (0, 0), image)
    new_image = new_image.convert('RGB')
    image.close()
    return np.array(new_image)


def get_contours(pic: np.array) -> Sequence[cv2.UMat]:
    pic = pic[:, :, ::-1]
    gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    value, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)
    # opencv 4.x:
    # cv2.CHAIN_APPROX_SIMPLE - контур хранится в виде отрезков
    # cv2.CHAIN_APPROX_NONE - контур хранится в виде точек
    cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return cnts


# Получение площади прямоугольной области в которой расположен путь
def get_area(path_arr: List[Segment], width: int, height: int) -> Area:
    max_x = 0
    min_x = width
    max_y = 0
    min_y = height
    for segment in path_arr:
        x = 0
        y = 0
        if isinstance(segment, M):
            x = segment.x
            y = segment.y
        elif isinstance(segment, C):
            x = segment.x2
            y = segment.y2
        max_x = max(max_x, x)
        min_x = min(min_x, x)
        max_y = max(max_y, y)
        min_y = min(min_y, y)
    area = Area(min_x, min_y, max_x, max_y)
    return area
