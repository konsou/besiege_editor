from edit_functions import *
from blocks import *
import math
import angle_tools

BESIEGE_MACHINES_DIR = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Besiege\\Besiege_Data\\SavedMachines\\"


tree = load_machine_file('empty_template.bsg')
root = tree.getroot()

blocks = root.find('Blocks')

block_length = 1
block_type = SMALL_WOODEN_BLOCK
circle_steps = 360

center_x = 1
center_y = radius = (circle_steps * block_length) / (2 * math.pi)
center_z = 1


def get_rotation_amount(rotation_degrees):
    while rotation_degrees >= 180:
        rotation_degrees -= 180
    while rotation_degrees < 0:
        rotation_degrees += 180

    # 0 -> 0
    # 90 -> 1
    # 180 -> 0
    # 360 -> 1

    ret_val = (rotation_degrees / 180 * 2)

    while ret_val > 1:
        ret_val -= 1
    while ret_val < -1:
        ret_val += 1
    return ret_val

# blocks.append(create_block(STARTING_BLOCK, position=(center_x, center_y, center_z)))
block_x = 1
for i in range(circle_steps):
    block_y = radius + angle_tools.calc_vy_from_angle(i, radius)
    block_z = radius + angle_tools.calc_vx_from_angle(i, radius)
    if i == 0:
        x_rotation = 1
    elif i == 90:
        x_rotation = 0
    elif i == 180:
        x_rotation = 1
    elif i == 270:
        x_rotation = 0
    else:
        x_rotation = 1 - (i / 360 * 6)
    print("Step: {}, rotation amount: {}".format(i, x_rotation))
    blocks.append(create_block(block_type, position=(block_x, block_y, block_z), rotation=(x_rotation, 0, 0, 1)))



# for x in range(5):
#     for y in range(5):
#         for z in range(5):
#             blocks.append(create_block(64, position=(x, y, z)))

# blocks.append(create_block(block_type, position=(0, 1, 1), rotation=(0, 0, 0, 0)))
# blocks.append(create_block(block_type, position=(5, 1, 1), rotation=(1, 0, 0, 0)))
# blocks.append(create_block(block_type, position=(10, 1, 1), rotation=(0, 0.7071068, 0, 0.7071068)))
# blocks.append(create_block(block_type, position=(15, 1, 1), rotation=(0, -0.7071068, 0, 0.7071068)))

save_machine_file(tree, BESIEGE_MACHINES_DIR + '!out.bsg')



# print(get_size_in_direction(root, 'x'))
# print(get_size_in_direction(root, 'y'))
# print(get_size_in_direction(root, 'z'))
# new_root = clone_machine(root, 'z')

# move_block(root.find('Blocks')[1], 'x', 5)
# move_block(root.find('Blocks')[0], 'y', -.5)
# move_block(root.find('Blocks')[0], 'z', 2.33)




