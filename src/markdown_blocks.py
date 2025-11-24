from enum import Enum
from htmlnode import ParentNode
from inline_markdown import text_to_children
from textnode import text_node_to_html_node, TextType, TextNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    markdown = markdown.strip()
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for block in raw_blocks:
        if block.strip() != "":
            blocks.append(block.strip())

    return blocks

def block_to_block_type(block):
    if len(block.split(" ")) > 1:
        heading_list = ["#" * i for i in range(1,7)]
        if block.split(" ")[0] in heading_list:
            return BlockType.HEADING
        
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    if block.startswith(">"):
        lines = block.split("\n")
        is_quote = True
        for line in lines:
            if not line.startswith(">"):
                is_quote = False
        if is_quote:
            return BlockType.QUOTE
        
    if block.startswith("- "):
        lines = block.split("\n")
        is_unordered_list = True
        for line in lines:
            if not line.startswith("- "):
                is_unordered_list = False
        if is_unordered_list:
            return BlockType.UNORDERED_LIST
    
    if block.startswith("1. "):
        lines = block.split("\n")
        is_ordered_list = True
        current_index = 1
        for line in lines:
            if not line.startswith(f"{current_index}. "):
                is_ordered_list = False
            current_index += 1
        if is_ordered_list:
            return BlockType.ORDERED_LIST
        
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    div_node = ParentNode(tag= "div", children = [])
    for block in blocks:
        node = ParentNode(tag = "div", children = [])
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            [header_block, text] = block.split(" ", 1)
            num = len(header_block)
            node.tag = f"h{num}"
            node.children = text_to_children(text.strip())

        if block_type == BlockType.CODE:
            text = block[3:-3]
            text = text.strip() + "\n"
            text_node = TextNode(text=text, text_type=TextType.CODE)
            node.tag = "pre"
            node.children = [text_node_to_html_node(text_node=text_node)]
        
        if block_type == BlockType.QUOTE:
            lines = block.split("\n")
            new_lines = [line[2:] for line in lines]
            text = "\n".join(new_lines)
            node.tag = "blockquote"
            node.children = text_to_children(text)
        
        if block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            new_lines = [line[2:] for line in lines]
            items = []
            for line in new_lines:
                list_item = ParentNode(tag= "li", children=text_to_children(text = line))
                items.append(list_item)
            node.tag = "ul"
            node.children = items
        
        if block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            new_lines = [line[3:] for line in lines]
            items = []
            for line in new_lines:
                list_item = ParentNode(tag= "li", children=text_to_children(text = line))
                items.append(list_item)
            node.tag = "ol"
            node.children = items

        if block_type == BlockType.PARAGRAPH:
            block = block.strip()
            text = " ".join(block.split("\n"))
            node.tag = "p"
            node.children = text_to_children(text=text)

        div_node.children.append(node)
    
    return div_node

        
    
        




            


        
    

    

