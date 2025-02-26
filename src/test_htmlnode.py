import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html(self):
        node1 = HTMLNode("p", "text", [], {"href": "https://www.google.com", "target": "_blank", })
        node1.props_to_html()
        #print(node1.props_to_html())

    def test2(self):
        node1 = HTMLNode("p", "text", [], {"href": "https://www.google.com", "target": "_blank", })
        #print(node1)
    
        
    def test_leaf(self):
        node = LeafNode("p", "this is text")
        #print(node.to_html())

    def test_leaf2(self):
        node = LeafNode("p", "this is text", {"href": "https://www.google.com", })
        #print(node.to_html())


    def test_leaf3(self):
        node = LeafNode(None, "this is text", {"href": "https://www.google.com", })
        #print(node.to_html())

    def test_no_tag(self):
        node = ParentNode()
        #print(node)

    def test_Parent1(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text"),], {"href": "https://www.something.com",})
        #print(node.to_html())

    def test_Parent2(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"),], {"href": "https://www.something.com",})
        #print(node.to_html())

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )




if __name__ == "__main__":
    unittest.main()