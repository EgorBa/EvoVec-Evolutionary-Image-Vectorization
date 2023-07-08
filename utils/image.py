import numpy as np
from PIL import Image
import cv2
import typing


def read_picture(path: str) -> np.array:
    image = Image.open(path)
    image = image.convert("RGBA")
    new_image = Image.new("RGBA", image.size, "WHITE")  # Create a white rgba background
    new_image.paste(image, (0, 0), image)
    new_image = new_image.convert('RGB')
    image.close()
    return np.array(new_image)


def get_contours(pic: np.array) -> typing.Sequence[cv2.UMat]:
    pic = pic[:, :, ::-1]
    gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    value, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)
    # opencv 4.x:
    # cv2.CHAIN_APPROX_SIMPLE - контур хранится в виде отрезков
    # cv2.CHAIN_APPROX_NONE - контур хранится в виде точек
    cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return cnts
