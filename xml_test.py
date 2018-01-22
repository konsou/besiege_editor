from edit_functions import *
from constants import *


tree = load_machine_file('empty_template.bsg')

make_circle(tree, radius=10, pos=(0, 10, 0))

set_machine_name(tree, "Circle")
save_machine_file(tree, BESIEGE_MACHINES_DIR + '!out.bsg')
# save_machine_file(tree)



