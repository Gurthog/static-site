from enum import Enum
from typing import Optional

from htmlnode import LeafNode


class TextType(Enum):
    BOLD = "bold"
    CODE = "code"
    IMAGE = "image"
    ITALIC = "italic"
    LINK = "link"
    TEXT = "text"


class TextNode:
    def __init__(
        self,
        text: str,
        text_type: TextType,
        url: Optional[str] = None
    ) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        same_text = self.text == other.text
        same_type = self.text_type == other.text_type
        same_url = self.url == other.url
        return (same_text and same_type and same_url)

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        delim_count = node.text.count(delimiter)
        if delim_count == 0:
            new_nodes.append(node)
            continue

        if delim_count % 2:
            raise Exception(f"invalid markdown: odd number of delimiter '{delimiter}'.")

        sections = node.text.split(delimiter)
        for i, text in enumerate(sections):
            # odd-indexed sections contain the target text type
            # "the *poop* dragon" -> ["the ", "poop", " dragon"]
            # "*the* poop dragon" -> ["", "the", " poop dragon"]
            # "the poop *dragon*" -> ["the poop ", "dragon", ""]
            if not text:
                continue
            if i % 2:
                new_nodes.append(TextNode(text, text_type))
            else:
                new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def text_node_to_html_node(node: TextNode) -> LeafNode:
    if node.text_type not in TextType:
        raise ValueError(f"invalid text_type: {node.text_type}")

    match node.text_type:
        case TextType.BOLD:
            return LeafNode("b", node.text)
        case TextType.CODE:
            return LeafNode("code", node.text)
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": node.url, "alt": node.text})
        case TextType.ITALIC:
            return LeafNode("i", node.text)
        case TextType.LINK:
            return LeafNode("a", node.text, {"href": node.url})
        case TextType.TEXT:
            return LeafNode(None, node.text)
        case _:
            raise ValueError(f"unhandled text type: {node.text_type}")

