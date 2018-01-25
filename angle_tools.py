import math
""" 
Copypasted from another project - most of this file is not needed and actually meant for Pygame. 

"""


def get_angle_in_radians(point1, point2):
    x_difference = point1[0] - point2[0]
    y_difference = point1[1] - point2[1]
    return math.atan2(y_difference, x_difference)


def get_angle_in_degrees(point1, point2):
    """
    Palauttaa kahden pisteen välisen kulman asteina väliltä 0 ... 360 (360 non-inclusive)
    0 = ylös
    90 = vasen
    180 = alas
    270 = oikea
    """
    angle_in_degrees = math.degrees(get_angle_in_radians(point1, point2))
    angle_in_degrees = 270 - angle_in_degrees
    angle_in_degrees = bound_angle_0_360(angle_in_degrees)
    return angle_in_degrees


def deg_to_rad_pygame(degrees):
    """ Antaa annetun kulman radiaaneina ja tekee pienen konversion Pygame-yhteensopivuuden takia """
    return math.radians(270 - degrees)


def bound_angle_0_360(angle):
    """ Muuttaa annetun kulman välille 0 ... 360 (360 non-inclusive) jos se ei vielä ole """
    while angle < 0:
        angle += 360
    while angle >= 360:
        angle -= 360
    return angle


def angle_difference(angle_current, angle_target):
    """
    Palauttaa nykyisen (angle_current) ja kohteen (angle_target) välisen pienimmän aste-eron
    Positiivinen = vastapäivään
    Negatiivinen = myötäpäivään
    """
    diff1 = angle_target - angle_current
    diff2 = angle_target + 360 - angle_current
    diff3 = angle_target - 360 - angle_current

    min_abs_diff = min(abs(diff1), abs(diff2), abs(diff3))
    if min_abs_diff == abs(diff1):
        return diff1
    elif min_abs_diff == abs(diff2):
        return diff2
    elif min_abs_diff == abs(diff3):
        return diff3
    else:
        raise ValueError("Konsolla bugi angle_difference -funktiossa")

    # return angle_target - angle_current


def calc_distance(point1, point2):
    x_difference = point1[0] - point2[0]
    y_difference = point1[1] - point2[1]
    return math.hypot(x_difference, y_difference)


def calc_vx_from_angle(angle, distance):
    try:
        return distance * math.cos(math.radians(angle))
    except TypeError as e:
        raise TypeError("in calc_vx_from_angle: {} \n angle: {} - distance: {}".format(e, angle, distance))


def calc_vy_from_angle(angle, distance):
    try:
        return distance * math.sin(math.radians(angle))
    except TypeError as e:
        raise TypeError("in calc_vx_from_angle: {} \n angle: {} - distance: {}".format(e, angle, distance))


def calc_pos_from_angle(angle, distance):
    """ Laskee pisteen, joka on määritetyn etäisyyden päässä määritetyssä suunnassa """
    return calc_vx_from_angle(angle, distance), calc_vy_from_angle(angle, distance)


def intify_tuple(input_tuple):
    """ Muuttaa tuplen itemit inteiksi """
    output_list = []
    for item in input_tuple:
        try:
            output_list.append(int(item))
        except ValueError as e:
            raise ValueError("in intify_tuple: values must be numeric \n {}".format(e))
    return tuple(output_list)


def points_average(point1, point2):
    """
    Palauttaa kahden pisteen välisen keskiarvopisteen (tuple)
    Käyttää integer divisionia ilman muita pyöristyksiä joten ei ehdottoman tarkka
    """
    return (point1[0] + point2[0]) // 2, (point1[1] + point2[1]) // 2
