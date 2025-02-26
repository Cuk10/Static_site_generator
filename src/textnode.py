from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text 
                and self.text_type == other.text_type 
                and self.url == other.url)
            

    def __repr__(self):
       return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            if delimiter not in node.text:
                raise Exception("That's invalid Markdown syntax")
            new = node.text.split(delimiter)
            i = 1
            for n in new:
                if i % 2 == 1:
                    new_nodes.append(TextNode(n, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(n, text_type))
                i += 1
        else:
            new_nodes.append(node)
    return new_nodes