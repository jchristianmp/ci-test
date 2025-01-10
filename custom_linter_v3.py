import os
import argparse
import re
import sys

import ast
import nbformat
from nbconvert import PythonExporter
from radon.complexity import cc_visit


def convert_notebook_to_script(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_content = nbformat.read(f, as_version=4)
    exporter = PythonExporter()
    script, _ = exporter.from_notebook_node(notebook_content)
    return script


######################################################################################
def check_cyclomatic_complexity(file_content,file_path,max_complexity=1):
    print(f"checking file: {file_content}")
    errors = 0
    tree = ast.parse(file_content)

    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

    for func in functions:
        complexities = cc_visit(func)

        for complexity in complexities:
            if complexity.complexity > max_complexity:
                print(f"{file_path}: Function '{func.name}' has complexity of {complexity.complexity}  > {max_complexity}")
                errors += 1

    return errors



def check_black_lines_blocks(file_path):
    errors = 0

    with open(file_path, 'r') as file:
        lines = file.readlines()


        for i in range(2, len(lines)):

            if re.match(r'^\s*(class|def|if|for)', lines[i]):
                if not re.match(r'^\s*$', lines[i -1]) or not re.match(r'^\s*$', lines[i - 2]):
                    print(f"{file_path}:{i:1}: Expected 2 blank lines")
                    errors += 1
                
                elif re.match(r'^\s*$', lines[i -3]):
                    print(f"{file_path}:{i:1}: To mamy lines (more than 2)")
                    errors += 1



def check_long_functions(file_content, file_path, max_lines):
    errors = 0
    print(f"checking file: {file_path}")
    tree = ast.parse(file_content)

    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

    for func in functions:
        lines = len(func.body)
        if lines > max_lines:
            print("error")
            errors += 1

    return errors


##########################################################



def lin_file(file_path, max_lines):
    errors = 0
    if file_path.endswith('.ipynb'):
        file_content = convert_notebook_to_script(file_path)
    else:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

    errors += check_cyclomatic_complexity(file_content, file_path)
    errors += check_long_functions(file_content, file_path, max_lines)

    return errors

    



def lin_directory(directory, max_lines):
    total_errors = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.ipynb'):
                file_path = os.path.join(root, file)
                total_errors += lin_file(file_path, max_lines)

    return total_errors
    



if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Custom description")
    parser.add_argument('directories', nargs='+', help="Directories to lint")
    parser.add_argument('--max-lines',type=int,default=80, help="max line length")
                

    args = parser.parse_args()

    total_errors = 0



    for directory in args.directories:
        total_errors += lin_directory(directory, args.max_lines)




    if total_errors>0:
        sys.exit(1)

    else:
        sys.exit(0)