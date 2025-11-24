from textnode import TextNode, TextType
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

import os
import shutil
import sys

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    if sys.argv[0]:
        basepath = "/"
    else:
        basepath = sys.argv[0]
    
    if os.path.exists(dir_path_public):
        print("Deleting public directory...")
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)


    print("Generating page...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)

main()
