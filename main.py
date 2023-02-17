import random
from tkinter import *
from turtle import *
from tkinter import ttk
import tree

import page
import themes
from page import Page


class NodeShape:
    shape = 'circle'
    size = 25

    def __init__(self, node=None, xy=(0, 0)):
        self.node = node if node is not None else None
        self.selected = False
        self.xy = (xy[0], xy[1])

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False


class Drawer(RawTurtle):
    def __init__(self, turtle_canvas):
        super().__init__(turtle_canvas)
        self.speed(0)
        self.width(3)
        self.getscreen().delay(0)
        self.fillcolor(theme.mg_color)
        self.pencolor(theme.fg_color)
        self.shape('circle')
        self.shapesize(0.5)
        self.up()
        self.center = (0, -275)
        self.goto_center()

    def goto_center(self):
        self.goto(self.pos()[0] - self.center[0], self.pos()[1] - self.center[1])

    def jump(self, pos=(0, 0)):
        self.up()
        self.goto((pos[0] - self.center[0], pos[1] - self.center[1]))

    def draw_abs(self, pos=(0, 0), action=None):
        self.jump((pos[0], pos[1]))
        self.down()
        action()
        self.up()

    def draw_rel(self, xoffset=0.0, yoffset=0.0, action=None):
        self.draw_abs(pos=(self.xcor() + xoffset + self.center[0], self.ycor() - yoffset + self.center[1]),
                      action=action)

    def draw_line(self, start=(0, 0), end=(0, 0)):
        # print(f"Start: {start}, End: {end}")
        self.draw_abs(pos=(start[0], start[1]),
                      action=lambda: self.goto(end[0] - self.center[0], end[1] - self.center[1]))

    def paste(self, val=""):
        self.draw_rel(xoffset=2, yoffset=-NodeShape.size / 2 - 1,
                      action=lambda: self.write(val, font=('Courier', 20, 'bold'), align='center'))

    def draw_node(self, parent=None, val=None, pos=()):
        child_pos = (pos[0], pos[1])

        self.draw_abs(pos=(child_pos[0], child_pos[1]),
                      action=lambda: self.draw_circle(NodeShape.size))
        if val is not None:
            self.draw_abs(pos=child_pos, action=lambda: self.paste(val))
        return NodeShape(xy=(child_pos[0], child_pos[1]))

    def draw_edge(self, parent=None, child=None):
        child_pos = (child.xy[0], child.xy[1])
        parent_pos = (parent.xy[0], parent.xy[1])

        pencil.draw_line((child_pos[0], child_pos[1]), (parent_pos[0], parent_pos[1]))

    def draw_circle(self, size):
        self.begin_fill()
        self.circle(size, steps=75)
        self.end_fill()


def draw_bst(root):
    traversal = bst.preorder_route()

    n = len(traversal)
    # depth = bst.get_depth(bst.root)
    padding = (NodeShape.size * 3, NodeShape.size * 4)
    subtree = 0
    parent = None

    for node in traversal[1:]:
        if node[0].data < root.data:
            subtree = -1

        elif node[0].data > root.data:
            subtree = 1

        if bst.has_inner_children(node[0]):
            print("Inner children")
            subtree = subtree * 5
            print(subtree)

        if parent is None:
            xnode = node[1] * padding[0] + (subtree * NodeShape.size * n / 5)
            ynode = node[2] * padding[1] - NodeShape.size * 2
            parent = pencil.draw_node(val=node[0].data[0],
                                      pos=(xnode, ynode))
            if node[0].left:
                pencil.draw_line((xnode, ynode), (xnode - NodeShape.size * 2.5 * n / 10, ynode - NodeShape.size * 2.25))
            if node[0].right:
                pencil.draw_line((xnode, ynode), (xnode + NodeShape.size * 2.5 * n / 10, ynode - NodeShape.size * 2.25))
        else:
            xnode = node[1] * padding[0] + (subtree * NodeShape.size * n / 5)
            ynode = node[2] * padding[1] - NodeShape.size * 2

            if node[0].left:
                pencil.draw_line((xnode, ynode), (xnode - NodeShape.size * 3, ynode - NodeShape.size * 3.25))
            if node[0].right:
                pencil.draw_line((xnode, ynode), (xnode + NodeShape.size * 3, ynode - NodeShape.size * 3.25))

            parent = pencil.draw_node(val=node[0].data[0],
                                      pos=(xnode,
                                           ynode))


def add_node(insert):
    insert()
    pencil.clear()
    root.configure(background=theme.bg_color, relief='flat')
    draw_bst(bst.root)


class GraphWindow:
    class Main(Page):

        def __init__(self, master=None, theme=None, **kw):
            super().__init__(master, theme=theme, **kw)
            self.chat_box_text = None
            self.input_buffer = ""

        def create(self):
            global pencil

            header = ttk.Label(self, text="PySocket")
            header.configure(style=theme.elements['h1'])

            elements_input_frame = ttk.Frame(self, width=50, padding=20)
            elements_input_frame.configure(style=theme.elements['entry'])
            elements_entry = themes.EntryXL(elements_input_frame, placeholder='[n...]',
                                            background='#aaaaaa',
                                            font=(theme.font, 16))

            elements_entry.configure(style=theme.elements['input'])

            send_button = ttk.Button(self, text="BST",
                                     command=lambda: add_node(
                                         lambda: bst.insert(int(elements_entry.get_valid_input()[0]),
                                                            value=NodeShape())),
                                     takefocus=False)
            send_button.configure(style=theme.elements['button'])

            canvas = Canvas(self, width=window_width, height=window_height)
            canvas.create_oval(0, 0, 230, 230, fill="#000000")
            screen = TurtleScreen(canvas)
            screen.bgcolor(theme.bg_color)

            pencil = Drawer(screen)

            self.pack()
            canvas.grid()
            header.grid(column=0, row=0, sticky='n')
            header.columnconfigure(0, weight=100)
            elements_input_frame.grid(column=0, row=2, sticky='nswe')
            elements_entry.grid(column=0, row=2, sticky='nswe')
            send_button.grid(column=0, row=2, sticky='nse')
            self.tkraise(canvas)
            self.pack_forget()

            # canvas = Canvas(root, width=window_width, height=window_height)
            # node = canvas.create_oval(0, 0, 230, 230, fill='#993333', background='#339933', width=4, outline='#333333')
            # text = canvas.create_text(node, 115, 115, text="0")
            #
            # #canvas.itemconfig(node, fill='#339933')
            # canvas.pack()


window_width = 1280
window_height = 720
root = Tk()
root.geometry(f"{window_width}x{window_height}")

pages = page.pages
window = GraphWindow()
theme = themes.Modern(root)
root.configure(background=theme.bg_color, relief='flat')

menu = pages['menu'] = window.Main(root, theme=theme, width=window_width, height=window_height)
pages['menu'].create()

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

style = theme.get_style()
style.theme_use(theme.get_name())

page.open_page(root, menu)
bst = tree.BST()
bst.generate([(4, NodeShape().shape), (3, NodeShape().shape), (7, NodeShape().shape), (5, NodeShape().shape)])
bst.randomize(node_count=40, value_range=(1, 200))
bst.insert(3, value=NodeShape())
draw_bst(bst.root)



root.mainloop()
