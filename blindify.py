"""Anonymizes a directory of files/assignments by creating a mapping of the original name to a random 64-bit value.

Usage:
    python blindify.py <-a | -d | -h> directory mapping.csv [-e entropy]

Author:
    Joshua Crotts - 04.17.2022
"""

from datetime import datetime

import argparse
import os
import random
import shutil
import sys

DEFAULT_ENTROPY = 64

def input_prompt(prompt, input_list):
    print(f"{prompt} Enter one of {str(input_list)}.")
    ans = input()
    while ans not in input_list:
        print(f"InputError: Please answer with one of {str(input_list)}.")
        ans = input()
    return ans

def anonymize(dir, outfile, entropy):
    # If an anonymized mapping already exists, don't overwrite it unless the user says to.
    exists = False
    if os.path.exists(outfile):
        ans = input_prompt("Warning: Could not create anonymized mapping file as one already exists. Do you want to overwrite it?", ["y", "n"])
        if ans == "n":
            sys.exit(0)
        else:
            exists = True
    # Create a copy, just to be sure...
    if exists:
        timenow = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        filename = f"{os.path.splitext(outfile)[0]}-copy-{timenow}.csv"
        print(f"Creating a copy of current output csv: {filename}")
        shutil.copy(outfile, filename)
        print("Copying complete!")

    # Create the mapping and rename the files/directories. Fix the directory if it ends with /.
    dir = dir.rstrip("/")
    mapping = {}
    for f in os.listdir(dir):
        id = random.getrandbits(entropy)
        mapping.update({id:f})
        try:
            os.rename(f"{dir}/{f}", f"{dir}/{str(id)}")
        except PermissionError:
            print(f"PermissionError: Cannot rename file {dir}/{f}: do you have the right privileges?")
            sys.exit(1)
    
    # Now output the mapping to a file. It's guaranteed to not exist.
    with open(outfile, "w") as f:
        for key in mapping:
            f.write(f"{key},{mapping[key]}\n")
    print(f"Successfully anonymized {dir} and created {outfile}.")

def deanonymize(dir, infile):
    # Create the dictionary from the mapping.
    mapping = {}
    try:
        with open(infile) as f:
            for line in f.readlines():
                line = line.rstrip("\n").split(",")
                # Check to see if the line is valid.
                if len(line) != 2:
                    print(f"ValueError: Invalid data in mapping file: {line}")
                    sys.exit(1)
                mapping.update({line[0]:line[1]})
    except IOError:
        print(f"IOError: Could not find input file {infile}")
        sys.exit(1)

    # Check to make sure that they're de-anonymizing the right folder. Just does a simple length check...
    if len(os.listdir(dir)) != len(mapping):
        ans = input_prompt(f"Warning: Input directory {dir} does not appear to match the directory with anonymized files. Do you want to continue?", ["y", "n"])
        if ans != 'y':
            sys.exit(0)

    # Now de-anonymize the files.
    for key in mapping:
        for f in os.listdir(dir):
            try:
                os.rename(f"{dir}/{key}", f"{dir}/{mapping[key]}")
                break
            except:
                print(f"FileNotFoundError: Could not find file {dir}/{key}")
                sys.exit(1)

    # Attempt to remove the output file.
    ans = input_prompt("De-anonymizing complete! Do you want to remove the anonymized mapping (.csv) file?", ["y", "n"])
    if ans == "y":
        os.remove(infile)
        print(f"Successfully Removed {infile}.")

def create_arg_parser():
    parser = argparse.ArgumentParser(description='blindify: Grade Assignments Anonymously!')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-a", action="store_true", dest="amode")
    group.add_argument("-d", action="store_true", dest="dmode")
    parser.add_argument("-i", action='store', metavar="Input File/Directory", type=str, nargs=1, dest="input_dir", required=True)
    parser.add_argument("-m", action='store', metavar="CSV Map", type=str, nargs=1, dest="csv_map", required=True)
    parser.add_argument("-e", action='store', metavar="Entropy in # of Bits", type=int, nargs=1, dest="entropy", default=DEFAULT_ENTROPY, required=False)
    return parser

if __name__ == "__main__":
    args = create_arg_parser().parse_args()
    if args.amode:
        anonymize(args.input_dir[0], args.csv_map[0], args.entropy)
    elif args.dmode:
        deanonymize(args.input_dir[0], args.csv_map[0])
