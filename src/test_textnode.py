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


    

if __name__ == "__main__":
    unittest.main()