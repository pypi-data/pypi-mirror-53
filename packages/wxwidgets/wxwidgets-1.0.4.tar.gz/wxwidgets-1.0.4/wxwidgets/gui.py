from wx import BoxSizer, VERTICAL
from wx import Frame, ID_ANY, App, EXPAND, Panel, EVT_CLOSE


class GUI(Frame):

    def __init__(self, *callbacks):
        Frame.__init__(self, None, ID_ANY, "CUT")
        self.Bind(EVT_CLOSE, lambda x: self.Destroy())
        root = Panel(self, EXPAND)
        sizer = BoxSizer(VERTICAL)

        elements = []
        for element in callbacks:
            sizer.Add(element, 1, EXPAND)

        root.SetSizer(sizer)


# Run the program
def init_gui(*callbacks):
    app = App(False)
    frame = GUI(callbacks)
    frame.Show()
    app.MainLoop()
