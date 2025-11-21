from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        current_text = old_node.text
        matches = extract_markdown_images(current_text)
        split_nodes = []
        for image in matches:
            split_text = current_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(split_text[0]) > 0: 
                split_nodes.append(TextNode(split_text[0], TextType.TEXT))
            split_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            current_text = split_text[1]
        if len(current_text) > 0:
            split_nodes.append(TextNode(current_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        current_text = old_node.text
        matches = extract_markdown_links(current_text)
        split_nodes = []
        for link in matches:
            split_text = current_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(split_text[0]) > 0: 
                split_nodes.append(TextNode(split_text[0], TextType.TEXT))
            split_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            current_text = split_text[1]
        if len(current_text) > 0:
            split_nodes.append(TextNode(current_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes

def text_to_textnodes(text):
    current_nodes = [TextNode(text, TextType.TEXT)]
    current_nodes = split_nodes_delimiter(current_nodes, "**", TextType.BOLD)
    current_nodes = split_nodes_delimiter(current_nodes, "_", TextType.ITALIC)
    current_nodes = split_nodes_delimiter(current_nodes, "`", TextType.CODE)
    current_nodes = split_nodes_image(current_nodes)
    current_nodes = split_nodes_link(current_nodes)
    return current_nodes


        

        