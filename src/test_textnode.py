import unittest

from textnode import (
    TextNode,
    TextType,
    split_nodes_delimiter,
    text_node_to_html_node,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_text_mismatch(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a hippo node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_type_mismatch(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_empty(self):
        nodes = []
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [])

    def test_bold(self):
        nodes = [TextNode("what the **frick** dude", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1], TextNode("frick", TextType.BOLD))

    def test_italic(self):
        nodes = [TextNode("what the _frick_ dude", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1], TextNode("frick", TextType.ITALIC))

    def test_multiple(self):
        nodes = [TextNode("not **freaking** _cool_ dude.", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes[1], TextNode("cool", TextType.ITALIC))
        newer_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        print(newer_nodes)
        self.assertEqual(newer_nodes[0], TextNode("not ", TextType.TEXT))
        self.assertEqual(newer_nodes[1], TextNode("freaking", TextType.BOLD))
        self.assertEqual(newer_nodes[3], TextNode("cool", TextType.ITALIC))
        self.assertEqual(newer_nodes[4], TextNode(" dude.", TextType.TEXT))

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("", TextType.LINK, "https://xkcd.com/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"href": "https://xkcd.com/"})

    def test_image(self):
        node = TextNode(
            "comic",
            TextType.IMAGE,
            "https://imgs.xkcd.com/comics/identity.png"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {
                "src": "https://imgs.xkcd.com/comics/identity.png",
                "alt": "comic",
            }
        )


if __name__ == "__main__":
    unittest.main()

