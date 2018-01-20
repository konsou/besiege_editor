import pygame
import math
import time
from pygame.locals import *
from colors import *

""" 
TOIMII! 

Päivitys 25.6.: toimii vielä paremmin

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


def angletools_debug_run():
    current_angle = 0
    current_radians = 0
    target_angle = 0
    target_radians = 0
    point1 = None
    circle_radius = 50
    circle_pos = None
    distance = None

    pygame.init()
    win = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Angle finding test")

    def show_text(pos, text, color=(255, 255, 255), bgcolor=(0, 0, 0), font_size=24):
        """ Utility-metodi tekstin näyttämiseen ruudulla """
        win = pygame.display.get_surface()
        font = pygame.font.Font(None, font_size)
        textimg = font.render(text, 1, color, bgcolor)
        win.blit(textimg, pos)

    center_point = (400, 300)

    running = True
    while running:
        mouse_position = pygame.mouse.get_pos()

        if point1 is None:
            halfway_point = points_average(center_point, mouse_position)
        else:
            halfway_point = points_average(center_point, point1)
            distance = calc_distance(center_point, halfway_point)
            circle_radius = int(max(mouse_position[0], distance + 1))
            # circle_radius = mouse_position[0]
            # x_side = math.sqrt((circle_radius ** 2) - ((calc_distance(center_point, halfway_point)) ** 2))
            x_side = math.sqrt((circle_radius ** 2) - (distance ** 2))
            angle_to_center_point = get_angle_in_degrees(halfway_point, center_point) + 90
            # print angle_to_center_point
            # circle_pos = (calc_vx_from_angle(angle_to_center_point, x_side),
            #               calc_vy_from_angle(angle_to_center_point, x_side))
            circle_pos = calc_pos_from_angle(angle_to_center_point, x_side)
            circle_pos = circle_pos[0] + halfway_point[0], circle_pos[1] + halfway_point[1]
            circle_pos = intify_tuple(circle_pos)
            degrees_difference = abs(get_angle_in_degrees(center_point, circle_pos) - get_angle_in_degrees(point1, circle_pos))
            # print degrees_difference

        angle_radians = get_angle_in_radians(mouse_position, center_point)
        angle_degrees = get_angle_in_degrees(mouse_position, center_point)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_PLUS:
                    circle_radius += 50
                elif event.key == K_MINUS:
                    circle_radius -= 50
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    point1 = event.pos
                elif event.button == 3:
                    target_angle = angle_degrees
                    target_radians = angle_radians

        # _vx = int(50 * math.cos(angle_radians))
        # _vy = int(50 * math.sin(angle_radians))
        vx = int(calc_vx_from_angle(angle_degrees, 50))
        vy = int(calc_vy_from_angle(angle_degrees, 50))

        vx_current = int(200 * math.cos(current_radians))
        vy_current = int(200 * math.sin(current_radians))
        vx_target = int(200 * math.cos(target_radians))
        vy_target = int(200 * math.sin(target_radians))

        # print(_vx, _vy)
        win.fill(0)

        # Point 1
        if point1 is not None:
            pygame.draw.circle(win, BLUE, point1, 5)

        # Circle center point
        if circle_pos is not None:
            pygame.draw.circle(win, RED, circle_pos, 5)
            pygame.draw.circle(win, YELLOW, circle_pos, circle_radius, 1)

        # Mouse pos
        pygame.draw.circle(win, YELLOW, mouse_position, 5)

        # Halfway point
        pygame.draw.circle(win, GREEN, halfway_point, 5)

        show_text((10, 10), str(center_point) + " - " + str(mouse_position))
        show_text((10, 30), str(angle_degrees))
        show_text((10, 50), "Circle radius: " + str(circle_radius))
        show_text((10, 70), "Distance: " + str(distance))
        # show_text((10, 90), "Difference   : " + str(angle_difference(current_angle, target_angle)))
        pygame.draw.circle(win, YELLOW, center_point, 5)
        # pygame.draw.circle(win, yellow, mouse_position, 5)
        # pygame.draw.line(win, yellow, center_point, mouse_position)
        # pygame.draw.line(win, red, center_point, (mouse_position[0], center_point[1]))
        # pygame.draw.line(win, red, mouse_position, (mouse_position[0], center_point[1]))
        # show_text(halfway_point, str(round(distance, 2)))
        # show_text((halfway_point[0], center_point[1]), str(round(x_difference, 2)))
        # show_text((mouse_position[0], halfway_point[1]), str(round(y_difference, 2)))
        pygame.display.flip()
        time.sleep(0.01)

    pygame.quit()

if __name__ == "__main__":
    angletools_debug_run()