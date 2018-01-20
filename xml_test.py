from edit_functions import *
import math

BESIEGE_MACHINES_DIR = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Besiege\\Besiege_Data\\SavedMachines\\"


tree = load_machine_file('empty_template.bsg')
root = tree.getroot()

blocks = root.find('Blocks')

for x in range(20):
    blocks.append(create_block(1, position=(x * 1.5, 1, 1), rotation=(math.radians(x), 0, 0, 1)))
# for x in range(5):
#     for y in range(5):
#         for z in range(5):
#             blocks.append(create_block(64, position=(x, y, z)))

save_machine_file(tree, BESIEGE_MACHINES_DIR + '!out.bsg')



# print(get_size_in_direction(root, 'x'))
# print(get_size_in_direction(root, 'y'))
# print(get_size_in_direction(root, 'z'))
# new_root = clone_machine(root, 'z')

# move_block(root.find('Blocks')[1], 'x', 5)
# move_block(root.find('Blocks')[0], 'y', -.5)
# move_block(root.find('Blocks')[0], 'z', 2.33)




