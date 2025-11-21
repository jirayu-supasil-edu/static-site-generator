from textnode import TextNode, TextType

from inline_markdown import split_nodes_image, split_nodes_link

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)

main()
