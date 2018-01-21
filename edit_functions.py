import lxml.etree as ET
from pyquaternion import Quaternion
import angle_tools
import copy
import uuid
import math
from blocks import *


def load_machine_file(filename):
    """
    Loads a Besiege xml machine file
    :param filename: name of file
    :return: ElementTree object
    """
    return ET.parse(filename)


def save_machine_file(tree, filename):
    """
    Saves an ElementTree object to a Besiege xml machine file
    :param tree: ElementTree object
    :param filename: name of file
    :return: None
    """
    print("Saving machine to \"{}\"...".format(filename))
    tree.write(filename, doctype='<?xml version="1.0" encoding="utf-8"?>', pretty_print=True)


def set_machine_name(root, new_name):
    """
    Sets a Besiege machines's name to a new value
    :param root: root of parsed xml, given by ElementTree tree.getroot()
    :param new_name: new name for the machine
    :return: None
    """
    root.find('Machine')['name'] = str(new_name)


def round_transform_values(root, round_ndigits=3):
    """
    Rounds all Transform values in a Besiege machine file (Position, Rotation, Scale)
    :param root: root of parsed xml, given by ElementTree tree.getroot()
    :param round_ndigits: number of digits to round to
    :return: None
    """
    for block in root.find('Blocks').findall('Block'):
        for transform_attrib in block.find('Transform').getchildren():
            for attrib_key in transform_attrib.attrib:
                transform_attrib.attrib[attrib_key] = str(round(float(transform_attrib.attrib[attrib_key]), round_ndigits))


def get_size_in_direction(root, direction):
    """
    Calculates the size of a machine in given direction
    :param root: root of parsed xml, given by ElementTree tree.getroot()
    :param direction: 'x', 'y' or 'z'
    :return: size of machine in given direction
    """
    direction = direction.lower()

    max_value = get_extreme_value(root, 'max', direction)
    min_value = get_extreme_value(root, 'min', direction)

    print("Max: {} - min: {}".format(max_value, min_value))
    return max_value - min_value


def get_extreme_value(root, minmax, direction):
    """
    Finds the extreme value of a machine in given direction
    :param root: root of parsed xml, given by ElementTree tree.getroot()
    :param minmax: 'min' or 'max' - to select if we want the minimum or the maximum of the value
    :param direction: 'x', 'y' or 'z'
    :return: selected extreme
    """
    direction = direction.lower()
    min_value = 99999999999
    max_value = -99999999999

    for block in root.find('Blocks').findall('Block'):
        value = float(block.find('Transform').find('Position').attrib[direction])
        if minmax == 'min':
            min_value = min(value, min_value)
        else:
            max_value = max(value, max_value)

    if minmax == 'min':
        return min_value
    else:
        return max_value


def clone_machine(tree, direction):
    """
    Clones the machine in given direction
    :param tree: ElementTree tree
    :param direction: 'x', 'y', 'z'
    :return: new tree with cloned data
    """
    # TODO: KESKEN

    tree_copy = copy.deepcopy(tree)
    root_copy = tree_copy.getroot()

    # max_value = get_extreme_value(root, 'max', direction)
    machine_size = get_size_in_direction(root, direction)

    index_counter = len(root.find('Blocks'))

    for block in root.find('Blocks').findall('Block'):
        root_copy.find('Blocks').insert(index_counter, block)
        index_counter += 1

    return root_copy


def move_block(block, direction, amount):
    """
    Moves a block (in place)
    :param block: Block xml element
    :param direction: 'x', 'y', 'z'
    :param amount: numeric value
    :return: Block xml element
    """
    direction = direction.lower()
    print('Moving block with guid {}'.format(block.attrib['guid']))
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
    # print(new_block.attrib)
    new_block.attrib['guid'] = str(uuid.uuid4())
    # print(new_block.attrib)
    return new_block


def create_block(block_id,
                 position=(0, 0, 0),
                 rotation=(0, 0, 0, 1),
                 scale=(1, 1, 1)):
    """
    Creates a new Block xml element
    :param block_id: block id (what block it is)
    :param position: x, y, z coordinates
    :param rotation: x, y, z, w coordinates
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
    new_block.append(ET.Element('Transform'))
    transform_element = new_block.find('Transform')
    transform_element.append(ET.Element('Position', attrib=position_dict))
    transform_element.append(ET.Element('Rotation', attrib=rotation_dict))
    transform_element.append(ET.Element('Scale', attrib=scale_dict))

    # Data element
    new_block.append(ET.Element('Data'))

    return new_block


def make_circle(blocks, radius, pos, block_id=SMALL_WOODEN_BLOCK, block_length=1):
    """
    Makes a circle of blocks, adds it to given xml Blocks element
    :param blocks: Blocks xml element - adds new blocks under it
    :param radius: radius of the circle
    :param pos: position (x, y, x) of the centre of the circle
    :param block: block id
    :param block_length: optional - block length
    :return:
    """

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



