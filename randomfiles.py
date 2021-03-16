from essential_generators import DocumentGenerator, MarkovTextGenerator, StatisticTextGenerator
import random

import argparse

# Create the parser
arg_parser = argparse.ArgumentParser(description='Create a random set of files and folders containing random data in a normal distribution')

# Add the arguments
arg_parser.add_argument('-path','-p',
                       metavar='path',
                       type=str,
                       help='the path to create files and folders')

arg_parser.add_argument('-size','-s',
                       metavar='Iiteger',
                       type=int,
                       help='the total size (bytes) to create')

arg_parser.add_argument('-numdirs','-nd',
                       metavar='integer',
                       type=int,
                       help='number of directories to create')

arg_parser.add_argument('-numfiles', '-nf',
                       metavar='integer',
                       type=int,
                       help='number of files to create')

args = arg_parser.parse_args()

root_path = args.path
TOTAL_STORAGE = args.size
NUM_FOLDERS = args.numdirs
NUM_FILES = args.numfiles

directory_type = "directory"
file_type = "file"

file_exts = ["png","wav","mov","jpg","mxf","docx","pproj","ai","psd","avi","aif"]


folder_tree = []

gen = StatisticTextGenerator()
# gen.init_word_cache(5000)
# gen.init_sentence_cache(5000)

# make a random name
def random_name():
      import string

      randname = gen.gen_word()

      #  up to for words in a name
      for i in range(0, random.randint(0, 3)):
            randname=f"{randname} {gen.gen_word()}"

      # strip any junk chars
      valid_chars = "-_ %s%s" % (string.ascii_letters, string.digits)
      return ''.join(c for c in randname if c in valid_chars)


# create some folders
for index in range(0, NUM_FOLDERS):
      folder_name = random_name()
      folder_tree.append({"type":directory_type, "name":folder_name, "contents":[]})


import numpy as np

# generate a distirbution leaning more towards larger proportion files
mu, sigma = 0.75, 0.1 # mean and standard deviation
s = np.random.default_rng().normal(mu, sigma, NUM_FILES)

# scale the distibution so we can make up files
file_unit_size = TOTAL_STORAGE / s.sum()
s_file = s * file_unit_size

# make some random filenames with extensions, drop them into folders randomly
for file_size in s_file:
      file_name = f"{random_name()}.{random.choice(file_exts)}"
      random.choice(folder_tree)["contents"].append({"type":file_type,"name":file_name,"size":round(file_size)})

# fold the folders in on each other, so theres a single folder at the top level and a random tree
for i in range(1,len(folder_tree)):
      moving_folder = folder_tree.pop()
      random.choice(folder_tree)["contents"].append(moving_folder)

# write out the files
import os

def writeout(file_path, file_name, file_size):
      # print(f"{file_path}/{file_name} ({file_size} bytes)")

      if not os.path.exists(file_path):
            try:
                  os.makedirs(file_path)
            except FileNotFoundError as e:
                  print(f"ERROR {file_path} could not be created!")
      try: 
            with open(f"{file_path}/{file_name}", 'wb') as fout:
                  fout.write(os.urandom(file_size))
      except FileNotFoundError as e:
            print(f"ERROR {file_path}/{file_name} not found")
            

# iterating write function
def iter_dir(root, dir_contents):
      for item in dir_contents:
            if item["type"] == file_type:
                  writeout(f"{root_path}/{root}", item["name"], item["size"])
            elif item["type"] == directory_type:
                  path = f"{root}/{item['name']}"
                  iter_dir(path, item["contents"])

# call the iterating write function
iter_dir("", folder_tree)                  

