import re
from enum import Enum
from textnode import *
from htmlnode import text_node_to_html_node, ParentNode

Markdown_marks = {
    "**": TextType.BOLD,
    "*": TextType.ITALIC,
    "_": TextType.ITALIC,
    "`": TextType.CODE,
}


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"



def split_nodes_delimiter(old_nodes, delimiter, text_type, user=None):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            if delimiter not in node.text:
                if user != 5:
                    raise Exception("That's invalid Markdown syntax")
                new_nodes.append(node)
            else:
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



def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT),]
    for mark in Markdown_marks:
        nodes = split_nodes_delimiter(nodes, mark, Markdown_marks[mark], 5)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
    

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    final = []
    for block in blocks:
        block = block.strip()
        if block != "":
            final.append(block)
    return final


def block_to_block_type(block):
    headings = ["#", "##", "###", "####", "#####", "######"]
    if block.split()[0] in headings:
        return BlockType.HEADING
    if block[:3] == "```" and block[::-1][:3] == "```":
        return BlockType.CODE
    blocks = block.split("\n")
    je1 = True
    for b in blocks:
        if b[:1] != ">":
            je1 = False
            break
    if je1:
        return BlockType.QUOTE
    je2 = True
    for b in blocks:
        if b[:2] != "- ":
            je2 = False
            break
    if je2:
        return BlockType.UNORDERED_LIST
    je3 = True
    i = 1
    for b in blocks:
        word = b.split()
        if word[0] != f"{i}." :
            je3 = False
            break
        i += 1
    if je3:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def block_type_to_tag(block_type):
    match(block_type):
        case(BlockType.PARAGRAPH):
            return "p"
        case(BlockType.HEADING):
            return "h"
        case(BlockType.CODE):
            return "code"
        case(BlockType.QUOTE):
            return "blockquote"
        case(BlockType.UNORDERED_LIST):
            return "ul"
        case(BlockType.ORDERED_LIST):
            return "ol"
        case _:
            raise ValueError


def text_to_children_nodes(text):
    new_text = " ".join(text.split("\n"))
    text_nodes = text_to_textnodes(new_text)
    children_html_nodes = []
    for text_node in text_nodes:
        children_html_nodes.append(text_node_to_html_node(text_node))
    return children_html_nodes


def text_to_lists(text):
    new_texts = text.split("\n")
    children = []
    for t in new_texts:
        t = " ".join(t.split()[1:])
        children.append(ParentNode("li", text_to_children_nodes(t)))
    return children


def get_heading_and_tag(text):
    num = len(text.split()[0])
    text = " ".join(text.split()[1:])
    return text, f"h{num}"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        tag = block_type_to_tag(block_type)
        if tag == "code":
            children = [text_node_to_html_node(TextNode(block.strip("`"), TextType.CODE)),]
            tag = "pre"
        elif tag == "ol" or tag == "ul":
            children = text_to_lists(block)
        elif tag == "h":
            text, tag = get_heading_and_tag(block)
            children = text_to_children_nodes(text)
        else:
            children = text_to_children_nodes(block)
        parent_nodes.append(ParentNode(tag, children))
    return ParentNode("div", parent_nodes)

