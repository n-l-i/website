
from subprocess import run
from shutil import rmtree
import pathlib
from os import listdir

current_path = pathlib.Path(__file__).parent.resolve()
paths = {}
paths["chess_ai"] = {"git_link":"https://github.com/n-l-i/chess_ai.git",
                     "local_directory":f"{current_path}/../Frontend/Content_pages/chess_ai/src"}

def main():
    for repo in paths.values():
        rmtree(repo['local_directory'])
        output = run(f"git clone {repo['git_link']} {repo['local_directory']}", shell=True, check=True)
        if output.returncode != 0:
            raise Exception
        make_imports_relative(repo['local_directory'])

def make_imports_relative(directory):
    for module_name in listdir(directory):
        if not module_name.endswith(".py"):
            continue
        module_name = module_name.replace(".py","")
        for file_name in listdir(directory):
            if not file_name.endswith(".py"):
                continue
            file_name = f"{directory}/{file_name}"
            with open(file_name, "r") as f:
                new_text = f.read()
                new_text = new_text.replace(f"import {module_name}", f"import .{module_name}")
                new_text = new_text.replace(f"from {module_name}", f"from .{module_name}")
            with open(file_name, "w") as f:
                f.write(new_text)

main()
