import os
import argparse
from glob import glob

import numpy as np
from PIL import Image

# parser = argparse.ArgumentParser()
# parser.add_argument(
#     "-v","--verbose", help="Increse output verbosity", 
#     action="store_true"
# )
# # parser.add_argument(
# #     "-o", "--out", dest="output_file", required=True, 
# #     help="Name of output file to save the work in"
# # )

# parser.add_argument(
#     "files", type=argparse.FileType('r'), nargs="+", 
#     help="List of files to combine. Seperate the file names with spaces") 
# args = parser.parse_args()
# if args.verbose:
#     print("Verbosity turned on")

# file_names = []

# for arg in args.files:
#     file_names.append(glob(arg))

# print()
# print(file_names)

#Does not currently have support to read files from folders recursively
parser = argparse.ArgumentParser(description='Read in a file or set of files, and return the result.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('path', nargs='+', help='Path of a file or a folder of files.')
parser.add_argument(
    "-o", "--out_file", dest="output_file", default="result", 
    help="Name of output file to save the work in"
)
parser.add_argument(
    "-d", "--out_dir", dest="output_dir", default="result", 
    help="The absolute path to the output directory to save the work in"
)
parser.add_argument('-e', '--extension', default='jpg', help='File extension to filter by.')
parser.add_argument('-w', '--wildcard', default='*', help='Wildcard to filter filenames. E.g. "f*" -> all files begining with "f"')
args = parser.parse_args()

# Parse paths
full_paths = [os.path.join(os.getcwd(), path) for path in args.path]
if args.output_dir == "result":
    args.output_dir = full_paths[0] + "\\" + args.output_dir

# create output dir if doesn't exist
if not os.path.exists(args.output_dir):
    os.mkdir(args.output_dir)

files = set()
for path in full_paths:
    if os.path.isfile(path):
        files.add(path)
    else:
        files |= set(glob(path + '/'+ args.wildcard + args.extension))
files = sorted(files)
print(files)

imgs    = [ Image.open(i) for i in files ]
# pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
imgs_comb = np.hstack( [np.asarray( i.resize(min_shape) ) for i in imgs ] )

# save that beautiful picture
imgs_comb = Image.fromarray( imgs_comb)
imgs_comb.save(args.output_dir + "\\" + args.output_file + "_horizontal." + args.extension)    

# for a vertical stacking it is simple: use vstack
imgs_comb = np.vstack( [np.asarray( i.resize(min_shape) ) for i in imgs ] )
imgs_comb = Image.fromarray( imgs_comb)
imgs_comb.save(args.output_dir + "\\" + args.output_file + "_vertical." + args.extension)    
