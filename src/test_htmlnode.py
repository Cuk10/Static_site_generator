import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html(self):
        node1 = HTMLNode("p", "text", [], {"href": "https://www.google.com", "target": "_blank", })
        node1.props_to_html()
        #print(node1.props_to_html())

    def test_2(self):
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

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text3(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    '''
    def test_text4(self):
        node = TextNode("This is a text node", "blabla")
        html_node = text_node_to_html_node(node)

    def test_text4_5(self):
        node = TextNode("This is a text node", 4.5)
        html_node = text_node_to_html_node(node)
    '''
        
    def test_text5(self):
        node = TextNode("This is a text node", TextType.IMAGE, "www.link.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.to_html(), '<img src="www.link.com" alt="This is a text node">')
    
    
#<img src="url/of/image.jpg" alt="Description of image">


if __name__ == "__main__":
    unittest.main()