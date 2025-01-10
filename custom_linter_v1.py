import os
import argparse
import re
import sys

def check_black_lines_block(file_path):
    errors = 0

    with open(file_path, 'r') as file:
        lines = file.readline()


        for i in range(2, len(lines)):

            if re.match(r'^\s*(class|def|if|for)', lines[i]):
                if not re.match(r'^\s*$', lines[i - 1]) or not re.match(r'^\s*$', lines[i - 2]):
                    print(f'{file_path}:{i:1}: Expected 2 blank lines')
                    errors += 1

                elif re.match(r'^\s*$', lines[i - 3]):
                    print(f'{file_path}:{i:1}: Too many lines (more than 2)')
                    errors += 1
    return errors


def lin_directory(directory):
    total_errors = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                total_errors += check_black_lines_block(file_path)
    return total_errors


if __name__=="__name__":
    parser = argparse.ArgumentParser(description="Custom description")
    parser.add_argument('directories', nargs='+', help="Directories to lint")

    args = parser.parse_args()

    total_errors = 0

    for directory in args.directories:
        total_errors += lin_directory(directory)

    if total_errors > 0:
        sys.exit(1)
    else:
        sys.exit(0)
