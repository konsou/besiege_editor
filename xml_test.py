from edit_functions import *
from constants import *


tree = load_machine_file(BESIEGE_MACHINES_DIR + 'grab-fly part.bsg')

print('Blocks loaded: {}'.format(len(tree.find('Blocks'))))

blocks = tree.getroot().find('Blocks')
# for block in blocks:
#     # print(block.attrib)
#     if block.attrib['id'] == str(DECOUPLER):

        # move_block(block, 'z', 0.1)
tree = clone_machine(tree, 'x', offset=-0.5)


save_machine_file(tree, BESIEGE_MACHINES_DIR + '!out.bsg')




