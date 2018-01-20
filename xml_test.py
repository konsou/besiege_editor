from edit_functions import *




root = tree.getroot()
blocks = root.find('Blocks')
copied_block = copy_block(blocks[0])
move_block(copied_block, 'x', 5)
blocks.insert(-1, copied_block)

round_transform_values(root, round_ndigits=3)
# print(get_size_in_direction(root, 'x'))
# print(get_size_in_direction(root, 'y'))
# print(get_size_in_direction(root, 'z'))
# new_root = clone_machine(root, 'z')

# move_block(root.find('Blocks')[1], 'x', 5)
# move_block(root.find('Blocks')[0], 'y', -.5)
# move_block(root.find('Blocks')[0], 'z', 2.33)




