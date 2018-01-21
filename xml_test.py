from edit_functions import *
from blocks import *
from pyquaternion import Quaternion
import math
import angle_tools

BESIEGE_MACHINES_DIR = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Besiege\\Besiege_Data\\SavedMachines\\"


tree = load_machine_file('empty_template.bsg')
root = tree.getroot()

blocks = root.find('Blocks')

make_circle(blocks, radius=5, pos=(0, 10, 0))
save_machine_file(tree, BESIEGE_MACHINES_DIR + '!out.bsg')



# print(get_size_in_direction(root, 'x'))
# print(get_size_in_direction(root, 'y'))
# print(get_size_in_direction(root, 'z'))
# new_root = clone_machine(root, 'z')

# move_block(root.find('Blocks')[1], 'x', 5)
# move_block(root.find('Blocks')[0], 'y', -.5)
# move_block(root.find('Blocks')[0], 'z', 2.33)




