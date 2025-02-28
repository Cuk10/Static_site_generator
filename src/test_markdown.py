import unittest

from markdown import *

class TestMarkdown(unittest.TestCase):
    
    def test_markdown_extract1(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted_images = extract_markdown_images(text)
        #print(extracted_images)
        # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extracted_images, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_markdown_extract2(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        extracted_links = extract_markdown_links(text)
        #print(extracted_links)
        # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extracted_links, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_split_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT),])

    def test_split_delimiter2(self):
        node = TextNode("_blabla_This is text with a _code block_ word _neki_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        #print(new_nodes)
        self.assertEqual(new_nodes, [TextNode("blabla", TextType.ITALIC), TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.ITALIC), TextNode(" word ", TextType.TEXT), TextNode("neki", TextType.ITALIC),])


    def test_split_delimiter3_error(self):
        node = TextNode("_blabla_This is text with a _code block_ word _neki_", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(str(context.exception), "That's invalid Markdown syntax")
        #print(new_nodes)
        



    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )


    def test_text_to_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes,
                         [
                            TextNode("This is ", TextType.TEXT),
                            TextNode("text", TextType.BOLD),
                            TextNode(" with an ", TextType.TEXT),
                            TextNode("italic", TextType.ITALIC),
                            TextNode(" word and a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" and an ", TextType.TEXT),
                            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                            TextNode(" and a ", TextType.TEXT),
                            TextNode("link", TextType.LINK, "https://boot.dev"),
                        ]
                        )


    def test_split_blocks(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
        """
        blocks = markdown_to_blocks(md)
        #print("============================================================================")
        #print(blocks)
        #print("============================================================================")
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                """- This is the first list item in a list block
- This is a list item
- This is another list item"""
            ],)
        

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_block_to_block_type1(self):
        block = """
### bloa bjdajjfhraufh fhukjahf z
dhaduaud

.ahkgrzj
ajhdjk 
*


"""
        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
        )

    def test_block_to_block_type2(self):
        block = """``` 
bloa bjdajjfhraufh fhukjahf z
dhaduaud

.ahkgrzj
ajhdjk 
*


```"""
        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE
        )

    def test_block_to_block_type3(self):
        block = """``` bloa bjdajjfhraufh fhukjahf z
dhaduaud

.ahkgrzj
ajhdjk 
*


"""
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type4(self):
        block = """>
> bloa bjdajjfhraufh fhukjahf z
>dhaduaud
>
>.ahkgrzj
>ajhdjk 
>*
>
>"""
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE
        )

    def test_block_to_block_type5(self):
        block = """- 
- bloa bjdajjfhraufh fhukjahf z
- dhaduaud
- 
- .ahkgrzj
- ajhdjk 
- *
- 
- """
        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST
        )

    def test_block_to_block_type6(self):
        block = """1. 
2. ### bloa bjdajjfhraufh fhukjahf z
3. dhaduaud
4. .ahkgrzj
5. ajhdjk 
6. *"""
        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST
        )



    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        

        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """

        
        ```This is text that _should_ remain
the **same** even with inline stuff
```"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    
    def test_md_to_html2(self):
        md = """
# Example Markdown File

## Introduction

This is an example of a Markdown file. Markdown is a lightweight markup language that you can use to add formatting elements to plaintext documents.

## Features

- **Easy to read and write**
- **Supports various formatting options**
- **Widely used for documentation and README files**

## Code Example

```python
# This is a simple Python program
print('Hello, World!')
```

## Conclusion

Markdown is a simple yet powerful tool for writing formatted text. It's commonly used in GitHub, documentation, and blogging platforms.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        #print("=====================================================")
        #print(html)
        #print("=====================================================")
        self.maxDiff = None
        self.assertEqual("<div><h1>Example Markdown File</h1><h2>Introduction</h2><p>This is an example of a Markdown file. Markdown is a lightweight markup language that you can use to add formatting elements to plaintext documents.</p><h2>Features</h2><ul><li><b>Easy to read and write</b></li><li><b>Supports various formatting options</b></li><li><b>Widely used for documentation and README files</b></li></ul><h2>Code Example</h2><pre><code>python\n# This is a simple Python program\nprint('Hello, World!')\n</code></pre><h2>Conclusion</h2><p>Markdown is a simple yet powerful tool for writing formatted text. It's commonly used in GitHub, documentation, and blogging platforms.</p></div>", html)


    def test_extract_title(self):
        title = extract_title("# Hello")
        self.assertEqual(title, "Hello")


    def test_extract_title2(self):
        title = extract_title("""

# Example Markdown File

## Introduction

This is an example of a Markdown file. Markdown is a lightweight markup language that you can use to add formatting elements to plaintext documents.

## Features

- **Easy to read and write**"""
                              )
        self.assertEqual(title, "Example Markdown File")


if __name__ == "__main__":
    unittest.main()