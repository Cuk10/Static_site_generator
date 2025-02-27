import re
from textnode import *





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
    return split_nodes_delete_0(new_nodes)


def split_nodes_delete_0(nodes):
    new_nodes = []
    for node in nodes:
        if not (node.text_type == TextType.TEXT and node.text == ""):
            new_nodes.append(node)
    return new_nodes



def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images


def extract_markdown_links(text):
    images = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if images == []:
            new_nodes.append(node)
        else:
            new = node.text
            for image in images:
                new = new.split(f"![{image[0]}]({image[1]})")
                new_nodes.append(TextNode(new[0], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                new = new[1]
            new_nodes.append(TextNode(new, TextType.TEXT))
    return split_nodes_delete_0(new_nodes)



def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if links == []:
            new_nodes.append(node)
        else:
            new = node.text
            for link in links:
                new = new.split(f"[{link[0]}]({link[1]})")
                new_nodes.append(TextNode(new[0], TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                new = new[1]
            new_nodes.append(TextNode(new, TextType.TEXT))
    return split_nodes_delete_0(new_nodes)