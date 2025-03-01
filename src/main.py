import os
import shutil
import sys
from textnode import TextNode, TextType
from markdown import markdown_to_html_node, extract_title
from htmlnode import *




def main():
    if len(sys.argv) == 1:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    from_static_to_docs()
    generate_pages_recursive("content", "template.html", "docs", basepath)


def from_static_to_docs():
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.mkdir("docs")
    copy_paste("static", "docs")


def from_static_to_public():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    copy_paste("static", "public")
    

def copy_paste(path, destination):
    files = os.listdir(path)
    for file in files:
        new_file = os.path.join(path, file)
        if os.path.isfile(new_file):
            shutil.copy(new_file, destination)
        else:
            new_destination = os.path.join(destination, file)
            os.mkdir(os.path.join(destination, file))
            copy_paste(new_file, new_destination)



def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        file_contents = f.read()
    with open(template_path) as f:
        template = f.read()
    html = markdown_to_html_node(file_contents).to_html()
    title = extract_title(file_contents)
    new_file = template.replace("{{ Title }}", title)
    new_file = new_file.replace("{{ Content }}", html)
    new_file = new_file.replace('href="/', 'href="' + basepath).replace('src="/', 'src="' + basepath)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(new_file)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    files = os.listdir(dir_path_content)
    for file in files:
        new_file = os.path.join(dir_path_content, file)
        dest_file = file.removesuffix(".md") + ".html"
        new_dest = os.path.join(dest_dir_path, dest_file)
        if os.path.isfile(new_file):
            generate_page(new_file, template_path, new_dest, basepath)
        else:
            new_dest = os.path.join(dest_dir_path, file)
            os.mkdir(os.path.join(dest_dir_path, file))
            generate_pages_recursive(new_file, template_path, new_dest, basepath)



main()