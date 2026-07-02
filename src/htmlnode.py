class HTMLNode:
    def __init__(
            self,
            tag: str = None,
            value: str = None,
            children: list[HTMLNode] = None,
            props: dict = None,
        ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        html = ""
        for attribute, value in self.props.items():
            html += f' {attribute}="{value}"'
        return html

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
            self,
            tag: str,
            value: str,
            props: dict = None,
        ) -> None:
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("All leaf nodes must have a value.")

        if not self.tag:
            return self.value

        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(
            self,
            tag: str,
            children: list[HTMLNode],
            props: dict = None,
        ) -> None:
        super().__init__(tag, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("All parent nodes must have a tag.")
        if self.children is None:
            raise ValueError("Children missing. Should someone call 911?")

        props = self.props_to_html()
        html = f"<{self.tag}{props}>"

        for node in self.children:
            html += node.to_html()

        html += f"</{self.tag}>"
        return html

