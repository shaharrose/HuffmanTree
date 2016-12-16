# Huffman compression
# Noam Pnueli & Shahar Rosenberg
# 29/10/2016
import sys

from HuffmanTree import HuffmanTree
from Parser import compress_file, file_data_to_frequency_list, compress_data, decompress_file, binary_to_file_data

# test_data = [(5, 1), (7, 2), (10, 3), (15, 4), (20, 5), (45, 6)]
# make_file_from_freq_list(test_data, 'tester.txt')

# out = open('compressed.huff', 'wb')
# out.write(b'' + binary_to_file_data(compress_data(huff, file_data)))

# print compress_data(huff, file_data)
# print file_to_bits('compressed.huff')

file_name = 'lord.bmp'
# compress_file(file_name)
decompress_file(file_name + '.huff')