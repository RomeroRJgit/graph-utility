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
    selected_color = '#e59965'
    border_color = '#332928'
    text_color = '#454142'
    padding = (size * 1.5, size * 1.5)

    def __init__(self, node, selected=False, color=None, outline=None):
        self.node = node
        self.pos = (0, 0)
        self.key = node.data[0]
        self.selected = selected
        self.color = self.fill_color if color is None else color
        self.outline = self.border_color if outline is None else outline
        self.shape_id = -1
        self.text_id = -1
        self.parent_edge = None


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
        self.nodes = {}

    def draw_node(self, node, parent=None):
        node.data[1]['shape'].pos = node_pos = self.get_graph_pos(node)


        xoffset = 0
        if node.data[0] < binary_search_tree.root.data[0]:
            xoffset = -1
        else:
            xoffset = 1
        xoffset = 0
        xoffset = xoffset * NodeShape.size * 2

        node.data[1]['shape'].shape_id = self.canvas.create_oval(node_pos[0] + xoffset + NodeShape.size, node_pos[1] + NodeShape.size, node_pos[0] + xoffset, node_pos[1],
                                    tag='node', fill=node.data[1]['shape'].color, width=NodeShape.border_width,
                                    outline=node.data[1]['shape'].outline)

        self.nodes[node.data[0]] = node.data[1]['shape']

        canvas.addtag_above(node.data[1]['shape'].shape_id, node.data[1]['shape'].shape_id)

        node.text_id = self.canvas.create_text(node_pos[0] + xoffset + NodeShape.size / 2, node_pos[1] + NodeShape.size / 2, tag='value', text=node.data[0], font=(theme.font, 16, 'normal'), state='disabled', fill=NodeShape.text_color)
        canvas.tag_bind(node.data[1]['shape'].shape_id, '<Button-1>', lambda e, key=node.data[0]: self.select_node(key))
        return node.data[1]['shape']

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
    def deselect_node(self, key):
        if key in self.nodes:
            node_shape = self.nodes[key]
            node_shape.selected = False
            self.canvas.itemconfig(node_shape.shape_id, fill=NodeShape.fill_color)

    def select_node(self, key):
        if key in self.nodes:
            node_shape = self.nodes[key]
            if node_shape.selected:
                self.deselect_node(key)
                return
            
            node_shape.selected = True
            self.canvas.itemconfig(node_shape.shape_id, fill=NodeShape.selected_color)

            route = []
            binary_search_tree.inorder_traversal(route, parent=node_shape.node)
            for node in route:
                print(node[1])
                #self.canvas.move(node[1]['shape'].shape_id, NodeShape.size, 0)

    def align_nodes(self):
        route = binary_search_tree.preorder_route()
        for node in route:
            print(node[0].data[0])
            node = node[0]
            if node.left and node.right:
                if node.right.left and node.right.left.data is not None:
                    print(f"left {node.right.left}")
                    print(f"left {node.right.left.data}")
                    left = node.right.left
                    left_shape = self.nodes[left.data[0]]
                    # self.canvas.itemconfig(left_shape.shape_id, fill='red')
                    print()
                    # for i in binary_search_tree.preorder_route(left):
                    #     self.canvas.move(self.nodes[i[0].data[0]].shape_id, -NodeShape.size * 2, 0)
                    #return
                if node.left.right and node.left.right.data is not None:
                    print(f"right {node.left.right}")
                    print(f"right {node.left.right.data}")
                    right = node.left.right
                    right_shape = self.nodes[right.data[0]]
                    # self.canvas.itemconfig(right_shape.shape_id, fill='green')
                    # for i in binary_search_tree.preorder_route(right):
                    #     self.canvas.move(self.nodes[i[0].data[0]].shape_id, NodeShape.size * 2, 0)



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
        node[0].data[1]['shape'] = NodeShape(node[0])

        if node[0] is binary_search_tree.root:
            node[0].data[1]['shape'].outline = '#eededd'

        graph_painter.draw_node(node[0])

        if last_parent:
            graph_painter.connect_node(node[0], node[0].parent)

        last_parent = node[0]
    graph_painter.align_nodes()


def add_node(key):
    node = binary_search_tree.insert(key)
    node.data[1]['shape'] = NodeShape(node)
    root.configure(background=theme.bg_color, relief='flat')
    draw_bst(binary_search_tree)


class GraphWindow:
    class Main(Page):

        def __init__(self, master=None, theme=None, **kw):
            super().__init__(master, theme=theme, **kw)

        def create(self):
            global canvas
            header = ttk.Label(self, text="BST")
            header.configure(style=theme.elements['h1'])

            elements_entry = themes.EntryXL(self, placeholder='     Enter a comma separated list of numbers')
            elements_entry.configure(style=theme.elements['input'], width=40, font=(theme.font, 16))

            insert_button = ttk.Button(self, text="Insert",
                                     command=lambda: add_node(int(elements_entry.get_valid_input()[0])),
                                     takefocus=False, padding='20 20')
            insert_button.configure(style=theme.elements['button'])

            delete_button = ttk.Button(self, text="Delete",
                                     command=lambda: add_node(int(elements_entry.get_valid_input()[0])),
                                     takefocus=False, padding='20 20')
            delete_button.configure(style=theme.elements['button'])

            search_button = ttk.Button(self, text="Search",
                                     command=lambda: graph_painter.select_node(int(elements_entry.get_valid_input()[0])),
                                     takefocus=False, padding='20 20')
            search_button.configure(style=theme.elements['button'])

            canvas = Canvas(self, width=canvas_width, height=canvas_height)

            canvas.configure(background=theme.bg_color, relief='flat')
            header.grid(column=0, row=0, sticky='nwse')
            elements_entry.grid(column=0, row=1, sticky='nwse')
            insert_button.grid(column=1, row=1, sticky='nwse')
            delete_button.grid(column=2, row=1, sticky='nwse', padx=10)
            search_button.grid(column=3, row=1, sticky='nwse', padx=10)
            canvas.grid(column=0, row=5, sticky='nswe')
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)
            #self.lower(canvas)
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

canvas = None
menu = pages['menu'] = window.Main(theme=theme, width=window_width, height=window_height)
pages['menu'].create()

root.columnconfigure(0, weight=1)

style = theme.get_style()
style.theme_use(theme.get_name())

graph_painter = GraphPainter(canvas)
page.open_page(root, menu)

binary_search_tree = tree.BST()
#binary_search_tree.generate([(4, NodeShape().shape), (3, NodeShape().shape), (7, NodeShape().shape), (5, NodeShape().shape)])
binary_search_tree.randomize(node_count=40, value_range=(1, 200))

draw_bst(binary_search_tree)

root.mainloop()
