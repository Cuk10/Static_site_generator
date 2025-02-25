import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLNode("p", "text", [], {"href": "https://www.google.com", "target": "_blank", })
        node1.props_to_html()
        print(node1.props_to_html())

    def test2(self):
        node1 = HTMLNode("p", "text", [], {"href": "https://www.google.com", "target": "_blank", })
        print(node1)

    





if __name__ == "__main__":
    unittest.main()