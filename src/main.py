import os
import shutil
from textnode import TextNode, TextType


def main():
    from_static_to_public()



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







main()