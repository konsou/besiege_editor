import lxml.etree as ET
import copy
import uuid


class PCParser(ET.TreeBuilder):
    def __init__(self):
        ET.TreeBuilder.__init__(self)
        # assumes ElementTree 1.2.X
        self._parser.CommentHandler = self.handle_comment

    def handle_comment(self, data):
        self._target.start(ET.Comment, {})
        self._target.data(data)
        self._target.end(ET.Comment)


class CommentedTreeBuilder(ET.TreeBuilder):
    def __init__(self, *args, **kwargs):
        super(CommentedTreeBuilder, self).__init__(*args, **kwargs)

    def comment(self, data):
        self.start(ET.Comment, {})
        self.data(data)
        self.end(ET.Comment)

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





# parser = PCParser()
# parser = ET.XMLParser(target=CommentedTreeBuilder())
tree = ET.parse('big can 002.bsg')  # , parser=parser)
root = tree.getroot()
blocks = root.find('Blocks')
print(blocks[0].attrib)
copied_block = copy_block(blocks[0])
print(copied_block.attrib)
move_block(copied_block, 'x', 5)
blocks.insert(1, copied_block)
print(blocks[0].attrib)
print(blocks[1].attrib)

round_transform_values(root, round_ndigits=3)
# print(get_size_in_direction(root, 'x'))
# print(get_size_in_direction(root, 'y'))
# print(get_size_in_direction(root, 'z'))
# new_root = clone_machine(root, 'z')

# move_block(root.find('Blocks')[1], 'x', 5)
# move_block(root.find('Blocks')[0], 'y', -.5)
# move_block(root.find('Blocks')[0], 'z', 2.33)

tree.write('out.bsg')


