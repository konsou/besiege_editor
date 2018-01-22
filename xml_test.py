from edit_functions import *
from constants import *


tree = load_machine_file('empty_template.bsg')
root = tree.getroot()

blocks = root.find('Blocks')

make_circle(blocks, radius=5, pos=(0, 10, 0))

set_machine_name(tree, "Circle")
save_machine_file(tree, BESIEGE_MACHINES_DIR + '!out.bsg')
save_machine_file(tree)



