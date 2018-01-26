import lxml.etree as ET
from pyquaternion import Quaternion
import os.path
import angle_tools
import copy
import uuid
import math
from blocks import *
from constants import *
from edit_functions import *

""" This file includes classes that help handle the Machine data """


class Block:
    def __init__(self, xml=None):
        """
        Inits a new Block object. Reads info from a parsed xml Block object if supplied.
        :param xml: parsed Block xml object (read from a .bsg Besiege machine file)
        """

        if xml is not None:
            # Use values from xml object
            self.id = int(xml.attrib['id'])
            self.guid = xml.attrib['guid']

            xml_transform = xml.find('Transform')
            xml_position = xml_transform.find('Position')
            xml_rotation = xml_transform.find('Rotation')
            xml_scale = xml_transform.find('Scale')

            self.position = {'x': float(xml_position.attrib['x']),
                             'y': float(xml_position.attrib['y']),
                             'z': float(xml_position.attrib['z'])}
            # Rotation is a quaternion
            self.rotation = {'x': float(xml_rotation.attrib['x']),
                             'y': float(xml_rotation.attrib['y']),
                             'z': float(xml_rotation.attrib['z']),
                             'w': float(xml_rotation.attrib['w'])}
            self.scale = {'x': float(xml_scale.attrib['x']),
                          'y': float(xml_scale.attrib['y']),
                          'z': float(xml_scale.attrib['z'])}

    def __repr__(self):
        return "<Block - id: {} ({}) - guid: {}>".format(self.id, block_name[self.id], self.guid)

    def print_block_info(self):
        """ Prints block info: id, guid, transform attributes """
        # This uses __repr__ to print block id, block name and guid
        print(self)
        print("Transform attributes:")
        print("    Position: {}".format(self.position))
        print("    Rotation: {}".format(self.rotation))
        print("    Scale: {}".format(self.scale))


if __name__ == '__main__':
    machine_filename = 'birdkiller.bsg'
    tree = load_machine_file(os.path.join(BESIEGE_MACHINES_DIR + machine_filename))
    blocks = get_machine_blocks(tree)
    block_obj = Block(blocks[1])
    block_obj.print_block_info()

