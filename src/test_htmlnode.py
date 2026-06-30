import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_values(self):
        node = HTMLNode(
            tag = "div",
            value = "poopdeck",
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "poopdeck")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_href(self):
        props = {"href": "https://xkcd.com/"}
        answer = ' href="https://xkcd.com/"'
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), answer)

    def test_props_to_html_multiple(self):
        props = {
            "href": "https://xkcd.com/",
            "target": "_blank",
        }
        answer = ' href="https://xkcd.com/" target="_blank"'
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), answer)


if __name__ == "__main__":
    unittest.main()

