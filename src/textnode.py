from enum import Enum


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
            url: str = None
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

