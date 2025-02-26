from textnode import TextNode, TextType


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        if not isinstance(self.props, dict):
            raise Exception("props must be a dictionary")
        return " " + " ".join(list(map(lambda x: f'{x}="{self.props[x]}"', self.props)))
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return f"{self.value}"
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}>{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError
        if self.children == None:
            raise ValueError
        children = ""
        for child in self.children:
            children += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children}</{self.tag}>"
    

def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case(TextType.TEXT):
            return LeafNode(value=text_node.text)
        case(TextType.BOLD):
            return LeafNode("b", text_node.text)
        case(TextType.ITALIC):
            return LeafNode("i", text_node.text)
        case(TextType.CODE):
            return LeafNode("code", text_node.text)
        case(TextType.LINK):
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case(TextType.IMAGE):
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("TextNode is None")