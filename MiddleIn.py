# Huffman compression
# Noam Pnueli & Shahar Rosenberg
import sys
from Parser import compress_file, decompress_file

if len(sys.argv) == 3:
    flag = sys.argv[1]
    file_name = sys.argv[2]

    if flag == '-c':
        compress_file(file_name)
    elif flag == '-d':
        decompress_file(file_name)
else:
    print "Usage: [flag] [file_name]\n"
    print "Flags:"
    print "\t-c: Compress file"
    print "\t-d: Decompress file"
    exit(1337)
