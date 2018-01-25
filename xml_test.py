from edit_functions import *
from constants import *


tree = load_machine_file(BESIEGE_MACHINES_DIR + '!grabfly4.bsg')

print('Blocks loaded: {}'.format(len(tree.find('Blocks'))))

blocks = get_machine_blocks(tree)
# for block in blocks:
#     move_block(block, 'z', -2)
#     # print(block.attrib)
#     if block.attrib['id'] == str(BRACE):
#         scale = block.find('Transform').find('Scale')
#         scale.attrib['x'] = '0.5'
#         scale.attrib['y'] = '0.5'
#         scale.attrib['z'] = '0.5'

        # move_block(block, 'z', 0.1)
tree = clone_machine(tree, 'x', offset=0)
tree = clone_machine(tree, 'x', offset=0)


save_machine_file(tree, BESIEGE_MACHINES_DIR + '!out.bsg')




