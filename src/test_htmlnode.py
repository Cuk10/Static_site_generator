import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html(self):
        node1 = HTMLNode("p", "text", [], {"href": "https://www.google.com", "target": "_blank", })
        node1.props_to_html()
        print(node1.props_to_html())

    def test2(self):
        node1 = HTMLNode("p", "text", [], {"href": "https://www.google.com", "target": "_blank", })
        print(node1)
    
        
    def test_leaf(self):
        node = LeafNode("p", "this is text")
        print(node.to_html())

    def test_leaf2(self):
        node = LeafNode("p", "this is text", {"href": "https://www.google.com", })
        print(node.to_html())


    def test_leaf3(self):
        node = LeafNode(None, "this is text", {"href": "https://www.google.com", })
        print(node.to_html())






if __name__ == "__main__":
    unittest.main()