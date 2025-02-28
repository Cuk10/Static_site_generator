import os
import shutil
from textnode import TextNode, TextType
from markdown import markdown_to_html_node, extract_title
from htmlnode import *


def main():
    from_static_to_public()
    generate_page("content/index.md", "template.html", "public/index.html")



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



def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        file_contents = f.read()
    with open(template_path) as f:
        template = f.read()
    html = markdown_to_html_node(file_contents).to_html()
    title = extract_title(file_contents)
    new_file = template.replace("{{ Title }}", title)
    new_file = template.replace("{{ Content }}", html)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(new_file)





main()