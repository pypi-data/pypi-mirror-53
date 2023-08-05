import urwid
import time
import threading
import webbrowser


state = {}


class FeedTreeWidget(urwid.TreeWidget):
    """ Display widget for leaf nodes """
    unexpanded_icon = urwid.AttrMap(urwid.TreeWidget.unexpanded_icon,
                                    'dirmark')
    expanded_icon = urwid.AttrMap(urwid.TreeWidget.expanded_icon,
                                  'dirmark')
    indent_cols = 4

    def __init__(self, node):
        self.__super.__init__(node)
        if self.get_node()._parent is not None:
            self.keypress(None, "-")
        self._w = urwid.AttrWrap(self._w, None)
        self.flagged = False
        self.update_w()

    def update_w(self):
        """Update the attributes of self.widget based on self.flagged.
        """
        if self.flagged:
            self._w.attr = 'flagged'
            self._w.focus_attr = 'flagged focus'
        else:
            self._w.attr = 'body'
            self._w.focus_attr = 'focus'

    def get_display_text(self):
        return self.get_node().get_value()['name']

    def get_feed_url(self):
        return self.get_node().get_value()['url']

    def selectable(self):
        """
        Allow selection of non-leaf nodes so children may be (un)expanded
        """
        return not self.is_leaf and self.get_node()._parent is not None

    def mouse_event(self, size, event, button, col, row, focus):
        if self.is_leaf or event != 'mouse press' or button != 1 or self.get_node()._parent is None:
            return False

        if row == 0 and col == self.get_indent_cols():
            self.expanded = not self.expanded
            self.update_expanded_icon()
            return True

        return False

    def keypress(self, size, key):
        """Handle expand & collapse requests (non-leaf nodes)"""
        if self.is_leaf:
            return key

        if key in ("+", "right"):
            self.expanded = True
            self.update_expanded_icon()
        elif key in ("-", "left"):
            self.expanded = False
            self.update_expanded_icon()
        elif self._w.selectable():
            return self.__super.keypress(size, key)
        else:
            return key

    def load_inner_widget(self):
        if self.is_leaf:
            return urwid.AttrMap(urwid.Text(self.get_display_text()), 'summary')
        else:
            return urwid.Text(self.get_display_text())

    def get_indented_widget(self):
        widget = self.get_inner_widget()
        div = urwid.Divider()
        if not self.is_leaf:
            widget = urwid.Columns([('fixed', 1,
                                     [self.unexpanded_icon, self.expanded_icon][self.expanded]),
                                    widget], dividechars=1)
        else:
            widget = urwid.Pile([widget, div])
        indent_cols = self.get_indent_cols()
        return urwid.Padding(widget,
                             width=('relative', 100), left=indent_cols, right=indent_cols)


class Node(urwid.TreeNode):
    """ Data storage object for leaf nodes """

    def load_widget(self):
        return FeedTreeWidget(self)


class FeedParentNode(urwid.ParentNode):
    """ Data storage object for interior/parent nodes """

    def load_widget(self):
        return FeedTreeWidget(self)

    def load_child_keys(self):
        data = self.get_value()
        return range(len(data['children']))

    def load_child_node(self, key):
        """Return either an Node or ParentNode"""
        childdata = self.get_value()['children'][key]
        childdepth = self.get_depth() + 1
        if 'children' in childdata:
            childclass = FeedParentNode
        else:
            childclass = Node
        return childclass(childdata, parent=self, key=key, depth=childdepth)

    def append_child_node(self, data):
        self._value["children"].extend(data["children"])


class CustomTree(urwid.TreeListBox):

    def unhandled_input(self, size, input):
        """Handle macro-navigation keys"""
        if input == 'left':
            return input
        elif input == '-':
            self.collapse_focus_parent(size)
        elif input == "enter":
            widget, pos = self.body.get_focus()
            webbrowser.open(widget.get_feed_url())
        else:
            return input


class FeedsTreeBrowser:
    palette = [
        ('body', 'white', 'black'),
        ('dirmark', 'light red', 'black', 'bold'),
        # ('title', 'default,bold', 'default', 'bold'),
        ('key', 'light cyan', 'black'),
        ('focus', 'light gray', 'dark blue', 'standout'),
        ('title', 'default,bold', 'default', 'bold'),
        ('summary', 'black', 'light gray'),
        # ('foot', 'light gray', 'black'),
        # ('flag', 'dark gray', 'light gray'),
        # ('error', 'dark red', 'light gray'),
    ]

    footer_text = [
        ('title', ""), "",
        ('key', "UP"), ",", ('key', "DOWN"), ",",
        # ('key', "PAGE UP"), ",", ('key', "PAGE DOWN"),
        "    ",
        ('key', "+"), ",",
        ('key', "-"), ",",
        ('key', "RIGHT"), ",",
        ('key', "LEFT"), "    ",
        ('key', "ENTER"), "    ",
        ('key', "Q"),
    ]

    def __init__(self, data=None):
        self.header = urwid.Text("2Feeds", align="left")
        self.footer = urwid.AttrMap(urwid.Text(self.footer_text),
                                    'foot')
        self.start = True

    def init_data(self, data, done=False):
        self.done = done
        if self.start:
            self.topnode = FeedParentNode(None)
            d_ = {"name": "/", "children": []}
            d_["children"].extend(data)
            self.topnode._value = d_
            self.tw = urwid.TreeWalker(self.topnode)
            self.listbox = CustomTree(self.tw)
            self.start = False
        else:
            d_ = self.topnode._value
            d_["children"].extend(data)
            self.topnode = FeedParentNode(d_)

    def generate_frame(self):
        return urwid.Padding(urwid.Frame(
            urwid.AttrMap(self.listbox, 'body'),
            header=urwid.AttrMap(self.header, 'title'),
            footer=self.footer), left=1, right=2)

    def store_state(self):
        # TODO:
        node = self.loop.widget.base_widget.body.base_widget._body.focus
        parent = node.get_parent()
        keys = parent.get_child_keys()
        for key in keys:
            state[key] = parent.get_child_widget(key).expanded

    def refresh(self, _loop, _data):
        """
        Redraw screen;
        TODO: is there a better way?
        """
        node = self.tw.get_focus()[1]
        key = node.get_key()
        # self.store_state()
        self.tw = urwid.TreeWalker(self.topnode.get_child_node(key))

        self.listbox = CustomTree(self.tw)
        self.loop.widget = self.generate_frame()
        if not self.done:
            self.loop.set_alarm_in(1, self.refresh)

    def main(self):
        """Run the program."""
        while not hasattr(self, 'listbox'):
            time.sleep(0.7)
            continue
        self.frame = urwid.AttrMap(self.generate_frame(), 'body')
        self.loop = urwid.MainLoop(self.frame, self.palette,
                                   unhandled_input=self.unhandled_input)
        self.loop.set_alarm_in(1, self.refresh)
        self.loop.run()

    def unhandled_input(self, k):
        if k in ('q', 'Q'):
            raise urwid.ExitMainLoop()
