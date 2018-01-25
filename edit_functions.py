import lxml.etree as ET
from pyquaternion import Quaternion
import os.path
import angle_tools
import copy
import uuid
import math
from blocks import *
from constants import *

""" Contains functions that help edit/create Besiege xml Machine files """


def load_machine_file(filename):
    """
    Loads a Besiege xml machine file
    :param filename: name of file
    :return: ElementTree object
    """
    return ET.parse(filename)


def save_machine_file(tree, filename=""):
    """
    Saves an ElementTree object to a Besiege xml machine file, adding doctype declaration.
    :param tree: ElementTree parsed xml object
    :param filename: name of file. If empty we use BESIEGE_MACHINES_DIR and machine name from xml.
    :return: None
    """
    if filename == "":
        filename = os.path.join(BESIEGE_MACHINES_DIR, tree.getroot().attrib['name'].lower() + ".bsg")
    print("Saving machine to \"{}\"...".format(filename))
    tree.write(filename, doctype='<?xml version="1.0" encoding="utf-8"?>', pretty_print=True)


def set_machine_name(tree, new_name):
    """
    Sets a Besiege machines's name to a new value
    :param tree: ElementTree parsed xml object
    :param new_name: new name for the machine
    :return: None
    """
    # root = Machine tag
    root = tree.getroot()
    root.attrib['name'] = str(new_name)


def round_transform_values(tree, round_ndigits=3):
    """
    Rounds all Transform values in a Besiege machine file (Position, Rotation, Scale)
    :param tree: ElementTree parsed xml object
    :param round_ndigits: number of digits to round to
    :return: None
    """
    root = tree.getroot()
    for block in root.find('Blocks').findall('Block'):
        for transform_attrib in block.find('Transform').getchildren():
            for attrib_key in transform_attrib.attrib:
                transform_attrib.attrib[attrib_key] = str(round(float(transform_attrib.attrib[attrib_key]), round_ndigits))


def get_size_in_direction(tree, direction):
    """
    Calculates the size of a machine in given direction
    :param tree: ElementTree parsed xml object
    :param direction: 'x', 'y' or 'z'
    :return: size of machine in given direction
    """
    root = tree.getroot()
    direction = direction.lower()

    max_value = get_extreme_value(tree, 'max', direction)
    min_value = get_extreme_value(tree, 'min', direction)

    print("Max: {} - min: {}".format(max_value, min_value))
    return max_value - min_value


def get_extreme_value(tree, minmax, direction, ignore_braces=True):
    """
    Finds the extreme value of a machine in given direction. Ignores braces by default.
    :param tree: ElementTree parsed xml object
    :param minmax: 'min' or 'max' - to select if we want the minimum or the maximum of the value
    :param direction: 'x', 'y' or 'z'
    :param ignore_braces: whether to ignore braces (True/False)
    :return: selected extreme
    """
    root = tree.getroot()
    direction = direction.lower()
    min_value = 99999999999
    max_value = -99999999999

    for block in root.find('Blocks').findall('Block'):
        # Ignore braces if set
        if ignore_braces and int(block.attrib['id']) == BRACE:
            continue

        value = float(block.find('Transform').find('Position').attrib[direction])
        if minmax == 'min':
            min_value = min(value, min_value)
        else:
            max_value = max(value, max_value)

    if minmax == 'min':
        return min_value
    else:
        return max_value


def clone_machine(tree, direction, offset=1, times=1):
    """
    Clones the machine in given direction
    :param tree: ElementTree tree
    :param direction: 'x', 'y', 'z'
    :param offset: this amount will be added to the 'direction' coordinate of every copied block
    :param times: how many times to clone the original
    :return: new tree with cloned data
    TODO: in-place?
    """
    tree_copy = copy.deepcopy(tree)
    root_copy = tree_copy.getroot()
    blocks_copy = root_copy.find('Blocks')
    root = tree.getroot()

    machine_size = get_size_in_direction(tree, direction)
    # max_value = get_extreme_value(tree, 'max', direction)
    for i in range(times):

        current_offset = (machine_size + offset) * (i + 1)
        # print("i: {}, current_offset: {}".format(i, current_offset))

        # index_counter = len(root.find('Blocks'))

        for block in root.find('Blocks').findall('Block'):
            copied_block = copy_block(block)
            move_block(copied_block, direction, current_offset)
            blocks_copy.append(copied_block)

    return tree_copy


def move_block(block, direction, amount):
    """
    Moves a block (in place)
    :param block: Block xml element
    :param direction: 'x', 'y', 'z'
    :param amount: numeric value
    :return: Block xml element
    TODO: Change signature to move_block(block, (amount_x, amount_y, amount_z))
    """
    direction = direction.lower()
    # print('Moving block with guid {}'.format(block.attrib['guid']))
    attrib_to_change = float(block.find('Transform').find('Position').attrib[direction])
    attrib_to_change += amount
    block.find('Transform').find('Position').attrib[direction] = str(attrib_to_change)

    return block


def copy_block(block):
    """
    Returns a copy of a Block with a new random uuid
    :param block: Block xml element
    :return: new Block xml element with a new uuid
    """

    new_block = copy.deepcopy(block)
    new_block.attrib['guid'] = str(uuid.uuid4())
    return new_block


def create_block(block_id,
                 position=(0, 0, 0),
                 rotation=(0, 0, 0, 1),
                 scale=(1, 1, 1)):
    """
    Creates a new Block xml element
    :param block_id: block id (what block it is)
    :param position: x, y, z coordinates
    :param rotation: x, y, z, w coordinates (quaternion)
    :param scale: x, y, z coordinates
    :return: new Block xml element
    """
    # Everything must be strings as this is xml
    block_id = str(block_id)
    position_dict = {'x': str(position[0]), 'y': str(position[1]), 'z': str(position[2])}
    rotation_dict = {'x': str(rotation[0]), 'y': str(rotation[1]), 'z': str(rotation[2]), 'w': str(rotation[3])}
    scale_dict = {'x': str(scale[0]), 'y': str(scale[1]), 'z': str(scale[2])}

    # Block element
    new_block = ET.Element('Block', attrib={'id': block_id, 'guid': str(uuid.uuid4())})

    # Transform element
    transform_element = ET.Element('Transform')
    new_block.append(transform_element)
    transform_element.append(ET.Element('Position', attrib=position_dict))
    transform_element.append(ET.Element('Rotation', attrib=rotation_dict))
    transform_element.append(ET.Element('Scale', attrib=scale_dict))

    # Data element
    new_block.append(ET.Element('Data'))

    return new_block


def get_machine_blocks(tree):
    """
    Selects all Block elements of a machine
    :param tree: ElementTree parsed xml object
    :return: list of all Block elements in given tree
    """
    return tree.getroot().find('Blocks').findall('Block')


def make_circle(tree, radius, pos, block_id=SMALL_WOODEN_BLOCK, block_length=1):
    """
    Makes a circle of blocks, adds it to given xml Blocks element
    :param tree: ElementTree parsed xml object
    :param radius: radius of the circle
    :param pos: position (x, y, z) of the centre of the circle
    :param block_id: optional - block id (defaults to small wooden block)
    :param block_length: optional - block length (default 1 - need to change manually if needed)
    :return:
    """
    blocks = tree.getroot().find('Blocks')

    circumference = 2 * math.pi * radius
    circle_steps = int(circumference / block_length)

    # print("Radius: {}".format(radius))
    # print("Circumference: {}".format(circumference))
    # print("Circle steps needed: {}".format(circle_steps))

    center_x = pos[0]
    # center_y = radius = (circle_steps * block_length) / (2 * math.pi)
    center_y = pos[1]
    center_z = pos[2]

    # blocks.append(create_block(STARTING_BLOCK, position=(center_x, center_y, center_z)))
    block_x = center_x
    for i in range(circle_steps):
        degrees = i / circle_steps * 360
        block_y = radius + angle_tools.calc_vy_from_angle(degrees, radius)
        block_z = radius + angle_tools.calc_vx_from_angle(degrees, radius)
        qua = Quaternion(axis=(1, 0, 0), degrees=90 - degrees)
        # print("Step: {}, rotation amount: {}".format(i, qua.degrees))
        blocks.append(create_block(block_id, position=(block_x, block_y, block_z), rotation=(qua[1], qua[2], qua[3], qua[0])))



