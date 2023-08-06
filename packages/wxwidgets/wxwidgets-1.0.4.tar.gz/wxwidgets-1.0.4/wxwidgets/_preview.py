from logging import info, error

from webcolors import hex_to_rgb
from wx import Panel, Colour, BoxSizer, HORIZONTAL, VERTICAL, EXPAND, ListCtrl, LC_REPORT, \
    BORDER_SUNKEN, TOP, EVT_LIST_COL_CLICK, EVT_LIST_END_LABEL_EDIT
from wx.lib.mixins.listctrl import ColumnSorterMixin, ListCtrlAutoWidthMixin, TextEditMixin
from wxwidgets._simple_button import SimpleButton


class Table(ListCtrl, ColumnSorterMixin, ListCtrlAutoWidthMixin, TextEditMixin):
    row_index = None
    _edit_callback = None
    _column_width = {}
    _default_width = 100

    # TODO make editable optional
    # TODO on click https://stackoverflow.com/questions/44719029/how-to-bind-wxpython-listctrl-with-onclick-button-event
    def __init__(self, parent, headers, size=(-1, 100), callback=None):
        super().__init__(parent, size=size, style=LC_REPORT | BORDER_SUNKEN)
        self._init_row_index()

        for i, text in enumerate(headers):
            self.InsertColumn(i, text)
            self.SetColumnWidth(i, self._default_width)  # Intial Column width
            self._column_width[i] = self._default_width

        ListCtrlAutoWidthMixin.__init__(self)  # clip last column to table size

        if callback:
            self._edit_callback = callback
            TextEditMixin.__init__(self)
            self.Bind(EVT_LIST_END_LABEL_EDIT, self.OnMixUpdate)

        ColumnSorterMixin.__init__(self, 3)
        self.itemDataMap = {}
        self.Bind(EVT_LIST_COL_CLICK, self.OnColClick, self)

    # https://stackoverflow.com/a/29590266/7062162
    def OnMixUpdate(self, event):
        # Set the changed data via the event.GetLabel not listCtrl.GetText which remains unchanged until we change it
        new_data = event.GetLabel()
        column = event.GetColumn()
        row = self.GetFocusedItem()
        if row < 0:
            error("FocusedItem is -1")
            row = 0
        row = self.GetItemData(row)

        if self._edit_callback:
            self._edit_callback(row, column, new_data)

        event.Skip()

    # used by the ColumnSorterMixin
    def OnColClick(self, event):
        event.Skip()

    # used by the ColumnSorterMixin
    def GetListCtrl(self):
        return self

    def _init_row_index(self):
        self.row_index = -1

    def add_line(self, data_list):

        if type(data_list) != list:
            raise ValueError

        self.row_index += 1
        self.itemDataMap[self.row_index] = tuple(data_list)

        new_item_index = self.InsertItem(self.row_index, data_list[0])
        self.update_row(data_list, self.row_index)
        self.SetItemData(self.row_index, self.row_index)  # used by the ColumnSorterMixin

        return self.row_index

    def update_last_cell(self, data, column):
        self.update_cell(data, column, self.row_index)

    def update_cell(self, data, column, row=0):
        if not data:
            raise ValueError
        if row > self.row_index:
            self.add_line([''] * self.GetColumnCount())

        self.SetItem(row, column, data)
        # self.update_width()

    def update_row(self, row_data, row):
        for i, data in enumerate(row_data):
            self.SetItem(row, i, data)
        # self.update_width()

    def update_width(self):  # TODO minimize execution

        # transpose array with zip
        data_map = self.itemDataMap.values()
        for i, column in enumerate(zip(*data_map)):
            self.SetColumnWidth(i, max(max(map(len, column)) * 6, self._default_width))

    def clear(self):
        self.DeleteAllItems()
        self._init_row_index()

    # color is a hex color value as string
    def set_row_color(self, id, color):
        col = hex_to_rgb(color)
        self.SetItemBackgroundColour(id, Colour(col))


class Preview(Panel):
    _listbox = None

    def __init__(self, parent, headers, buttons, border=10, edit_callback=None):
        super().__init__(parent)

        self._listbox = Table(self, headers=[str(x.value) for x in headers], callback=edit_callback)

        # CONTROL FRAMES
        button_frame = Panel(self)
        button_sizer = BoxSizer(HORIZONTAL)
        for callback, text in buttons:
            button_sizer.Add(SimpleButton(button_frame, text_button=text, callback=callback), flag=TOP, border=border)
        button_frame.SetSizer(button_sizer)
        # ALIGN
        sizer = BoxSizer(VERTICAL)
        sizer.Add(self._listbox, 1, EXPAND)
        sizer.Add(button_frame)
        self.SetSizer(sizer)

    def add_lines(self, data):
        for line in data:
            info("LINE: " + str(line))
            self._listbox.add_line(line)

    def add_line(self, data_list):
        self._listbox.add_line(data_list)

    def update_cell(self, data, column, row):
        self._listbox.update_cell(data, column, row)

    def update_row(self, data, row):
        self._listbox.update_row(data, row)

    def update_last_cell(self, data, column):
        self._listbox.update_last_cell(data, column)

    def clear(self):
        self._listbox.clear()

    def set_row_color(self, id, color):
        self._listbox.set_row_color(id, color)
