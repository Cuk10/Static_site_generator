import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq1(self):
        node3 = TextNode("test", TextType.TEXT, "http.cool")
        node4 = TextNode("test", TextType.TEXT, "http.col")
        self.assertNotEqual(node3, node4)

    def test_noteq2(self):
        node3 = TextNode("test", TextType.TEXT)
        node4 = TextNode("test", TextType.TEXT)
        self.assertEqual(node3, node4)
    
    def test_noteq3(self):
        node3 = TextNode("test", TextType.TEXT, "http.cool")
        node4 = TextNode("test", TextType.BOLD, "http.cool")
        self.assertNotEqual(node3, node4)


    def test_split_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT),])

    def test_split_delimiter2(self):
        node = TextNode("_blabla_This is text with a _code block_ word _neki_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        #print(new_nodes)
        self.assertEqual(new_nodes, [TextNode("", TextType.TEXT), TextNode("blabla", TextType.ITALIC), TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.ITALIC), TextNode(" word ", TextType.TEXT), TextNode("neki", TextType.ITALIC), TextNode("", TextType.TEXT),])

if __name__ == "__main__":
    unittest.main()