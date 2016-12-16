# https://www.siggraph.org/education/materials/HyperGraph/video/mpeg/mpegfaq/huffman_tutorial.html
# https://www.cs.usfca.edu/~brooks/S04classes/cs245/lectures/lecture10.pdf
# http://stackoverflow.com/questions/759707/efficient-way-of-storing-huffman-tree


class HuffmanTree(object):  # object = life
    def __init__(self, freq_tuple, root=None):
        """
        :param freq_dict: frequency - value tuple. i.e. ((1, 'a'), (2, 'g'))
        """
        if root:
            self._root = root
        else:
            freq_dup = list(freq_tuple)
            freq_dup = HuffmanTree._sort_freq(freq_dup)

            while len(freq_dup) > 1:
                a, b = freq_dup[0], freq_dup[1]
                freq_dup = freq_dup[2:]
                a_node = HuffmanTree._node_or_value(a)
                b_node = HuffmanTree._node_or_value(b)
                parent = Node(a[0] + b[0], None)
                parent.left = a_node
                parent.right = b_node
                self._root = parent
                freq_dup.append((parent.freq, parent))
                freq_dup = HuffmanTree._sort_freq(freq_dup)

    def get_root(self):
        return self._root

    def get_huffman_code_for_value(self, val):
        return self._get_huffman_code_for_value(self._root, val)

    def get_value_for_huffman_code(self, binary):
        curr = self._root
        while not curr.is_leaf():
            if str(binary[0]) == "0":
                curr = curr.left
            elif str(binary[0]) == "1":
                curr = curr.right
            binary = binary[1:]
        return binary, curr.val

    def encode_tree(self):
        return Node.encode_node(self._root)

    def _get_huffman_code_for_value(self, node, val):
        if node is None:
            return None
        if node.right is not None and node.right.val == val:
            return "1"
        if node.left is not None and node.left.val == val:
            return "0"
        right_val = self._get_huffman_code_for_value(node.right, val)
        left_val = self._get_huffman_code_for_value(node.left, val)
        if right_val is not None:
            return "1" + right_val
        if left_val is not None:
            return "0" + left_val
        return None

    @staticmethod
    def _sort_freq(freq_list):
        return sorted(freq_list, key=lambda x: x[0])

    @staticmethod
    def _node_or_value(something):
        return something[1] if isinstance(something[1], Node) else Node(something[0], something[1])


class Node(object):
    def __init__(self, freq, val):
        self.freq = freq
        self.val = val
        self.right, self.left = None, None

    def is_leaf(self):
        return self.right is None and self.left is None

    @staticmethod
    def encode_node(node):
        if node.is_leaf():
            return [1, node.val]
        else:
            return [0] + Node.encode_node(node.left) + Node.encode_node(node.right)

    def __str__(self):
        return 'Freq: {}\t Val: {}'.format(self.freq, self.val)
