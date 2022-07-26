from math import pi

from vsdx import Shape


def get_x_center(shape: Shape) -> float:
    return float(shape.center_x_y[0])


def get_y_center(shape: Shape) -> float:
    return float(shape.center_x_y[1])


def get_width(shape: Shape) -> float:
    if 'Width' in shape.cells:
        return float(shape.cells['Width'].value)

    if 'Width' in shape.master_shape.cells:
        return float(shape.master_shape.cells['Width'].value)


def get_height(shape: Shape) -> float:
    if 'Height' in shape.cells:
        return float(shape.cells['Height'].value)

    if 'Height' in shape.master_shape.cells:
        return float(shape.master_shape.cells['Height'].value)


def get_angle(shape: Shape) -> float:
    return float(shape.cells['Angle'].value)


def normalize_angle(angle: float) -> float:
    return angle + 2 * pi if angle < 0 else angle


def get_normalized_angle(shape: Shape) -> float:
    return normalize_angle(get_angle(shape))


def get_limits(shape: Shape) -> tuple:
    center_x = get_x_center(shape)
    center_y = get_y_center(shape)
    width = get_width(shape)
    height = get_height(shape)

    return (center_x - (width / 2), center_y - (height / 2)), \
           (center_x + (width / 2), center_y + (height / 2)) 
