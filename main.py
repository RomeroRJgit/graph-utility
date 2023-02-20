import random
from tkinter import *
from tkinter import ttk
import tree

import page
import themes
from page import Page


class NodeShape:
    size = 60
    border_width = 4
    fill_color = '#a96945'
    selected_color = '#C57945'
    border_color = '#332928'
    text_color = '#454142'
    padding = (size * 1.5, size * 1.5)

    def __init__(self, node):
        self.node = node if node is not None else None
        self.pos = (0, 0)
        self.key = node.data[0]
        self.selected = False
        self.color = self.fill_color
        self.shape_id = -1
        self.text_id = -1
        self.parent_edge = None

    def update(self):
        if self.selected:
            self.color = self.selected_color


class EdgeShape:
    width = 4
    color = '#694925'

    def __init__(self, child):
        self.child = child

class GraphPainter:
    def __init__(self, canvas):
        self.canvas = canvas
        self.offset = 0, 220
        self.center = canvas_width / 2 - NodeShape.size * 1.5, canvas_height / 2 - self.offset[1] - NodeShape.size * 1.5
        self.nodes = []

    def draw_node(self, node, parent=None):
        node.data[1]['shape'] = NodeShape(node)
        node.data[1]['shape'].pos = node_pos = self.get_graph_pos(node)
        print(binary_search_tree.is_inner(node))

        xoffset = 0
        if node.data[0] < binary_search_tree.root.data[0]:
            xoffset = -1
        else:
            xoffset = 1
        xoffset = 0
        xoffset = xoffset * NodeShape.size * 2

        node.shape_id = self.canvas.create_oval(node_pos[0] + xoffset + NodeShape.size, node_pos[1] + NodeShape.size, node_pos[0] + xoffset, node_pos[1],
                                    tag='node', fill=node.data[1]['shape'].color, width=NodeShape.border_width,
                                    outline=NodeShape.border_color)
        self.nodes.append(node.shape_id)
        #canvas.addtag('selected', 'withtag', 'node')

        node.text_id = self.canvas.create_text(node_pos[0] + xoffset + NodeShape.size / 2, node_pos[1] + NodeShape.size / 2, tag='value', text=node.data[0], font=(theme.font, 16, 'normal'), fill=NodeShape.text_color)
        canvas.tag_bind('node', '<Button-1>', lambda e, obj=node: self.test(obj))
        return node.data[1]['shape']

    def test(self, node):
        print(node)
        print(node.data[1]['shape'])
        print(node.data[1]['shape'].color)
        node.data[1]['shape'].color = 'red'
        node.data[1]['shape'].update()
        self.update_graph(binary_search_tree)
    def erase_node(self, node):
        self.canvas.delete(node.shape_id)
        self.canvas.delete(node.text_id)

    def connect_node(self, child, parent):
        child_pos = child.data[1]['shape'].pos
        parent_pos = parent.data[1]['shape'].pos

        xoffset = 0
        if child.data[0] < binary_search_tree.root.data[0]:
            xoffset = -1
        else:
            xoffset = 1
        xoffset = 0
        xoffset = xoffset * NodeShape.size * 2

        self.canvas.create_line(child_pos[0] + xoffset + NodeShape.size / 2, child_pos[1] - (NodeShape.border_width - 1), parent_pos[0] + xoffset + NodeShape.size / 2, parent_pos[1] + NodeShape.size + (NodeShape.border_width - 1), width=EdgeShape.width, fill=EdgeShape.color)

    def draw_edge(self, start=(0, 0), end=(0, 0)):
        start_pos = self.get_pos_offset(start)
        end_pos = self.get_pos_offset(end)
        self.canvas.create_line(start_pos[0], start_pos[1], end_pos[0], end_pos[1])

    def get_pos_offset(self, pos=()):
        return pos.xy[0] - self.center[0], pos.xy[1] - self.center[1]

    def get_graph_pos(self, node):
        x_translation = node.index * NodeShape.padding[0] + NodeShape.size
        y_translation = node.level * NodeShape.padding[1] + NodeShape.size

        return x_translation + self.center[0], y_translation + self.center[1]

    def select_node(self, node):
        node.selected = True
        node.update()
        self.canvas.itemconfig(node, fill='#339933')
        self.update_graph(binary_search_tree)

    def deselect_node(self, node):
        node.selected = False
        node.update()
        self.canvas.itemconfig(node, fill='#339933')

    def update_graph(self, bst):
        traversal = bst.preorder_route()
        for node in traversal[1:]:
            if node[0].data[1] and type(node[0].data[1]['shape']) is NodeShape:
                shape = node[0].data[1]['shape']
                shape.update()
                self.canvas.itemconfig(shape.shape_id, fill=shape.color)


def draw_bst(bst):
    root_node = bst.root

    traversal = bst.preorder_route()

    last_parent = None
    for node in traversal:
        graph_painter.draw_node(node[0])
        if last_parent:
            graph_painter.connect_node(node[0], node[0].parent)

        last_parent = node[0]


def add_node(key):
    node = binary_search_tree.insert(key)
    node.data[1]['shape'] = NodeShape(node)
    root.configure(background=theme.bg_color, relief='flat')
    draw_bst(binary_search_tree)


class GraphWindow:
    class Main(Page):

        def __init__(self, canvas, master=None, theme=None, **kw):
            super().__init__(master, theme=theme, **kw)
            self.canvas = canvas

        def create(self):
            header = ttk.Label(self, text="BST")
            header.configure(style=theme.elements['h1'])

            elements_input_frame = ttk.Frame(self, width=50, padding=20)
            elements_input_frame.configure(style=theme.elements['entry'], padding='20 20')
            elements_entry = themes.EntryXL(elements_input_frame, placeholder='Enter a comma separated list of numbers',
                                            background=theme.text_color,
                                            font=(theme.font, 18))

            elements_entry.configure(style=theme.elements['input'])

            send_button = ttk.Button(self, text="Create",
                                     command=lambda: add_node(int(elements_entry.get_valid_input()[0])),
                                     takefocus=False)
            send_button.configure(style=theme.elements['button'])

            self.canvas.configure(background=theme.bg_color, relief='flat')
            #header.grid(column=0, row=0, sticky='n')
            #header.columnconfigure(0, weight=100)
            elements_input_frame.grid(column=0, row=2, sticky='nswe')
            elements_entry.grid(column=0, row=2, sticky='nswe')
            send_button.grid(column=1, row=2, sticky='nswe')
            self.canvas.pack()
            self.tkraise(self.canvas)
            self.grid_forget()


window_width = 1280
window_height = 720
canvas_width = 1280
canvas_height = 640

root = Tk()
root.geometry(f"{window_width}x{window_height}")

pages = page.pages
window = GraphWindow()
theme = themes.Modern(root)
root.configure(background=theme.bg_color, relief='flat')

canvas = Canvas(root, width=canvas_width, height=canvas_height)
menu = pages['menu'] = window.Main(canvas, theme=theme, width=window_width, height=window_height)
pages['menu'].create()

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

style = theme.get_style()
style.theme_use(theme.get_name())

graph_painter = GraphPainter(canvas)
page.open_page(root, menu)

binary_search_tree = tree.BST()
#binary_search_tree.generate([(4, NodeShape().shape), (3, NodeShape().shape), (7, NodeShape().shape), (5, NodeShape().shape)])
binary_search_tree.randomize(node_count=40, value_range=(1, 200))

draw_bst(binary_search_tree)

root.mainloop()
