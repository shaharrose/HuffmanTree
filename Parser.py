import os
import progressbar
from bitstring import BitArray
from HuffmanTree import Node, HuffmanTree


def file_to_frequency_list(file_path):
    handle = open(file_path, 'rb')
    data = handle.read()
    handle.close()
    return file_data_to_frequency_list(data)


def file_data_to_frequency_list(file_data):
    temp_dict = {}
    for c in file_data:
        if c not in temp_dict:
            temp_dict[c] = 1
        else:
            temp_dict[c] += 1

    freq_list = []
    for key, value in temp_dict.iteritems():
        freq_list.append((value, key))
    return freq_list


def make_file_from_freq_list(freq_list, file_name):
    data = ''
    for freq, val in freq_list:
        data += str(val) * freq
    open(file_name, 'wb').write(data)


def compress_data(tree, data):
    compressed = []
    for c in data:
        compressed.append(tree.get_huffman_code_for_value(c))
    return ''.join(compressed)


def binary_to_file_data(binary):
    mod = len(binary) % 8
    if mod > 0:
        binary = '0' * (8 - mod) + binary
    data = []
    for index in range(len(binary) / 8):
        substring = binary[index * 8: index * 8 + 8]
        byteval = BitArray(bin=substring)
        data.append(byteval.uint)
    return bytearray(data)


def _bytes_from_file(filename, chunksize=8192):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                for b in chunk:
                    yield b
            else:
                break


def file_to_bits(file_name):
    final_bits = ""
    for b in _bytes_from_file(file_name):
        binary = str(bin(ord(b))[2:])
        # if len(binary) < 8:
        #     binary = '0' * (8 - len(binary)) + binary
        final_bits += binary
    return final_bits


def data_to_bits(data):
    final_bits = ""
    for index, b in enumerate(data):
        binary = str(bin(ord(b))[2:])
        if len(binary) < 8 and index > 0:
            binary = '0' * (8 - len(binary)) + binary
        final_bits += binary
    return final_bits


def tree_to_file_header(huff):
    encoded = huff.encode_tree()
    bytess = []
    for d in encoded:
        if isinstance(d, str):
            bytess.append(ord(d))
        else:
            bytess.append(d)
    return bytearray(bytess + ['\x03', '\x03'])


def compress_file(uncompressed):
    print 'Compressing'
    bar = progressbar.ProgressBar(maxval=100, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    file_handle = open(uncompressed, 'rb')
    file_data = file_handle.read()
    file_handle.close()
    huff = HuffmanTree(file_data_to_frequency_list(file_data))

    header = tree_to_file_header(huff)
    binary_data = '1' + compress_data(huff, file_data)
    compressed = binary_to_file_data(binary_data)

    # file_name = '.'.join(uncompressed.split('.')[:-1]) + '.huff'
    file_name = uncompressed + '.huff'
    new_file_data = header + compressed
    try:
        os.remove(file_name)
    except:
        pass
    new_handle = open(file_name, 'wb')
    new_handle.write(new_file_data)
    new_handle.close()

    bar.finish()


def decompress_file(compressed_file_name):
    print 'Decompressing'
    bar = progressbar.ProgressBar(maxval=100, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    file_handle = open(compressed_file_name, 'rb')
    file_data = file_handle.read()
    file_handle.close()

    # h_length = ord(str(file_data)[0])
    # only_header = bytearray(str(file_data)[1:h_length + 1])
    # compressed_data = file_data[h_length + 1:]
    split = str(file_data).split('\x03\x03')
    only_header = bytearray(split[0])
    compressed_data = '\x03\x03'.join(split[1:])
    huff = header_to_tree(only_header)

    compressed_bits = data_to_bits(compressed_data)[1:]
    original_length = float(len(compressed_bits))
    uncompressed_data = ""
    while len(compressed_bits) > 0:
        bar.update(100 * (1 - (len(compressed_bits) / original_length)))
        binary, data = huff.get_value_for_huffman_code(compressed_bits)
        compressed_bits = binary
        uncompressed_data += data

    new_file = 'out/' + '.'.join(compressed_file_name.split('.')[:-1])
    
    new_handler = open(new_file, 'wb')
    new_handler.write(uncompressed_data)
    new_handler.close()

    bar.finish()


def _header_generator(header):
    for c in header:
        yield c


def header_to_tree(header):
    root = _read_node(_header_generator(header))
    return HuffmanTree([], root)


def _read_node(gen):
    try:
        nex = gen.next()
    except:
        return None
    if int(nex) == 1:
        return Node(0, chr(gen.next()))
    left = _read_node(gen)
    right = _read_node(gen)
    n = Node(0, None)
    n.left = left
    n.right = right
    return n
