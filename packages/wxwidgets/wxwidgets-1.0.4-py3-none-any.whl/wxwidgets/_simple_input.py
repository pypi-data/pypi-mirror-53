from wx import Panel, TextCtrl, HORIZONTAL, BoxSizer, StaticText


class SimpleInput(Panel):

    def __init__(self, parent, label, initial=""):
        super().__init__(parent)

        sizer = BoxSizer(HORIZONTAL)
        self._text_input = TextCtrl(self)
        self._text_input.SetValue(initial)
        sizer.Add(self._text_input)
        sizer.Add(StaticText(self, label=label))
        self.SetSizer(sizer)

    def get_value(self):
        return self._text_input.GetValue()